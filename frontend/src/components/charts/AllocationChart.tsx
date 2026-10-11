import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatNumber } from '@/lib/utils';
import type { AllocationResponse } from '@/lib/types';
import { TrendingUp } from 'lucide-react';

interface AllocationChartProps {
  data: AllocationResponse;
}

export function AllocationChart({ data }: AllocationChartProps) {
  const chartData = [
    { name: 'Optimizer', coverage: data.optimizer.total_coverage, color: '#2563eb' }, // blue-600
    { name: 'Highest HWSI', coverage: data.baseline_hwsi.total_coverage, color: '#9ca3af' }, // gray-400
    { name: 'Proportional', coverage: data.baseline_proportional.total_coverage, color: '#cbd5e1' } // slate-300
  ];

  const diff = data.baseline_hwsi.total_coverage > 0 
    ? ((data.optimizer.total_coverage - data.baseline_hwsi.total_coverage) / data.baseline_hwsi.total_coverage) * 100 
    : 0;

  return (
    <div className="w-full min-w-0 overflow-hidden">
      <div className="flex items-center justify-between gap-2 mb-2">
        <div>
          <h4 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
            Protected Coverage
          </h4>
          <p className="text-[11px] text-gray-500">Estimated population protected</p>
        </div>
        {diff > 0 && (
          <div className="flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200/80 px-2 py-0.5 rounded-full shrink-0">
            <TrendingUp className="w-3 h-3" />
            <span>+{diff.toFixed(1)}% gain</span>
          </div>
        )}
      </div>

      <div className="w-full h-36 min-w-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={chartData} 
            layout="vertical" 
            margin={{ top: 4, right: 12, left: -10, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f3f4f6" />
            <XAxis 
              type="number" 
              tickFormatter={(v) => formatNumber(v, 0)} 
              tick={{ fontSize: 10, fill: '#6b7280' }}
              axisLine={{ stroke: '#e5e7eb' }}
              tickLine={false}
            />
            <YAxis 
              dataKey="name" 
              type="category" 
              width={90} 
              tick={{ fontSize: 11, fill: '#374151', fontWeight: 500 }}
              axisLine={{ stroke: '#e5e7eb' }}
              tickLine={false}
            />
            <Tooltip 
              formatter={(value: number) => [`${formatNumber(value, 0)} people`, 'Protected Coverage']}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.96)',
                backdropFilter: 'blur(4px)',
                borderRadius: '8px',
                border: '1px solid #e5e7eb',
                fontSize: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                padding: '6px 10px',
              }}
            />
            <Bar dataKey="coverage" radius={[0, 4, 4, 0]} barSize={16}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-1.5 pt-2 border-t border-gray-100 text-center">
        <div className="bg-blue-50/60 rounded p-1">
          <div className="text-[10px] text-blue-700 font-medium truncate">Optimizer</div>
          <div className="text-xs font-bold text-blue-900 tabular-nums">
            {formatNumber(data.optimizer.total_coverage, 0)}
          </div>
        </div>
        <div className="bg-gray-50 rounded p-1">
          <div className="text-[10px] text-gray-600 font-medium truncate">Highest HWSI</div>
          <div className="text-xs font-bold text-gray-800 tabular-nums">
            {formatNumber(data.baseline_hwsi.total_coverage, 0)}
          </div>
        </div>
        <div className="bg-gray-50 rounded p-1">
          <div className="text-[10px] text-gray-600 font-medium truncate">Proportional</div>
          <div className="text-xs font-bold text-gray-800 tabular-nums">
            {formatNumber(data.baseline_proportional.total_coverage, 0)}
          </div>
        </div>
      </div>
    </div>
  );
}
