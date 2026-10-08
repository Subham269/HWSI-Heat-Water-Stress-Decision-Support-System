import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatNumber } from '@/lib/utils';
import type { AllocationResponse } from '@/lib/types';

interface AllocationChartProps {
  data: AllocationResponse;
}

export function AllocationChart({ data }: AllocationChartProps) {
  const chartData = [
    { name: 'Optimizer', coverage: data.optimizer.total_coverage, color: '#3b82f6' }, // blue-500
    { name: 'Highest HWSI', coverage: data.baseline_hwsi.total_coverage, color: '#9ca3af' }, // gray-400
    { name: 'Proportional', coverage: data.baseline_proportional.total_coverage, color: '#d1d5db' } // gray-300
  ];

  return (
    <div className="w-full h-48 mt-4">
      <h4 className="text-sm font-semibold mb-2 text-center text-gray-700">Resource Allocation Comparison</h4>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" tickFormatter={(v) => formatNumber(v, 0)} />
          <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 12 }} />
          <Tooltip formatter={(value: number) => formatNumber(value, 0)} />
          <Bar dataKey="coverage" radius={[0, 4, 4, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
