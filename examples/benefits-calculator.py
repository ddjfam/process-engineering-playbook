"""Calculate a synthetic capacity-value scenario. Requires Python 3 only.

Usage: python examples/benefits-calculator.py [path/to/inputs.json]
Capacity value is not cash savings. The model assumes constant run-rate months.
"""
import json
import math
from pathlib import Path
import sys


def calculate(data):
    before, after = data['baseline'], data['redesigned']
    assumptions = data['benefit_assumptions']
    for section in (before, after, assumptions):
        for name, value in section.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f'{name} must be a finite, non-negative number')
    for period in (before, after):
        for denominator in ('completed_requests', 'valid_survey_responses'):
            if period[denominator] <= 0:
                raise ValueError(f'{denominator} must be positive')
        for count in ('rework_requests', 'within_sla_requests'):
            if period[count] > period['completed_requests']:
                raise ValueError(f'{count} cannot exceed completed_requests')
        if period['favorable_survey_responses'] > period['valid_survey_responses']:
            raise ValueError('favorable responses cannot exceed valid responses')
    for rate in ('adoption_rate', 'capacity_realization_rate'):
        if assumptions[rate] > 1:
            raise ValueError(f'{rate} must be between zero and one')
    if after['handling_minutes'] > before['handling_minutes']:
        raise ValueError('This capacity-release model requires non-increasing handling time')

    metrics = {}
    for label, period in (('baseline', before), ('redesigned', after)):
        metrics[label] = {
            'mean_elapsed_hours': period['mean_elapsed_hours'],
            'handling_minutes': period['handling_minutes'],
            'rework_rate': period['rework_requests'] / period['completed_requests'],
            'sla_attainment_rate': period['within_sla_requests'] / period['completed_requests'],
            'favorable_survey_rate': period['favorable_survey_responses'] / period['valid_survey_responses'],
        }
    gross_hours = assumptions['monthly_volume'] * (before['handling_minutes'] - after['handling_minutes']) / 60
    adopted_hours = gross_hours * assumptions['adoption_rate']
    usable_hours = adopted_hours * assumptions['capacity_realization_rate']
    monthly_value = usable_hours * assumptions['loaded_hourly_cost_usd']
    months = assumptions['run_rate_months']
    period_value = monthly_value * months
    recurring_cost = assumptions['recurring_monthly_cost_usd'] * months
    return {
        'status': data['status'],
        'financial_treatment': 'Capacity value only; no cash savings recognized by this model',
        'metrics': metrics,
        'gross_hours_released_monthly': gross_hours,
        'adoption_adjusted_hours_monthly': adopted_hours,
        'usable_capacity_hours_monthly': usable_hours,
        'capacity_value_usd_monthly': monthly_value,
        'modeled_run_rate_months': months,
        'capacity_value_usd_for_period': period_value,
        'recurring_cost_usd_for_period': recurring_cost,
        'one_time_implementation_cost_usd': assumptions['one_time_implementation_cost_usd'],
        'net_capacity_value_equivalent_usd_for_period': period_value - recurring_cost - assumptions['one_time_implementation_cost_usd'],
    }


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('benefits-inputs.json')
    try:
        result = calculate(json.loads(path.read_text(encoding='utf-8')))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f'Cannot calculate benefits: {exc}')
    print(json.dumps(result, indent=2))
