import { cn } from '@/lib/utils';

interface DataBadgeProps {
  type: 'LIVE' | 'STATIC' | 'PERIODIC' | 'MOCK' | 'STALE' | string;
}

export function DataBadge({ type }: DataBadgeProps) {
  const colors: Record<string, string> = {
    LIVE: 'bg-green-100 text-green-800 border-green-200',
    STATIC: 'bg-gray-100 text-gray-800 border-gray-200',
    PERIODIC: 'bg-blue-100 text-blue-800 border-blue-200',
    MOCK: 'bg-amber-100 text-amber-800 border-amber-200',
    STALE: 'bg-red-100 text-red-800 border-red-200',
  };

  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border', colors[type] || colors['STATIC'])}>
      {type}
    </span>
  );
}
