import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(num: number, decimals: number = 2) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num);
}

export function formatPercent(num: number, decimals: number = 1, isFraction: boolean = true) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(isFraction ? num : num / 100);
}

export function bandToColor(band: string) {
  switch (band) {
    case 'Low': return '#22c55e';
    case 'Moderate': return '#eab308';
    case 'High': return '#f97316';
    case 'Very High': return '#ef4444';
    default: return '#94a3b8';
  }
}
