import { useState } from 'react';
import { useAllocation } from '@/hooks/useAllocation';
import { AllocationChart } from '@/components/charts/AllocationChart';
import { formatNumber } from '@/lib/utils';

interface AllocationPanelProps {
  extraDays: number;
}

export function AllocationPanel({ extraDays }: AllocationPanelProps) {
  const [tankers, setTankers] = useState(20);
  const [coolingUnits, setCoolingUnits] = useState(10);
  const { allocate, result, isLoading, error } = useAllocation();

  const handleRun = () => {
    allocate(tankers, coolingUnits, extraDays);
  };

  return (
    <div className="p-4 flex flex-col h-full overflow-y-auto">
      <h3 className="text-lg font-bold mb-4">Resource Allocation</h3>
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-1">Water Tankers</label>
          <div className="flex items-center gap-2">
            <button className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded" onClick={() => setTankers(Math.max(0, tankers - 1))}>-</button>
            <input type="number" className="border rounded px-2 py-1 w-20 text-center" value={tankers} onChange={e => setTankers(parseInt(e.target.value) || 0)} />
            <button className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded" onClick={() => setTankers(tankers + 1)}>+</button>
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Cooling/ORS Units</label>
          <div className="flex items-center gap-2">
            <button className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded" onClick={() => setCoolingUnits(Math.max(0, coolingUnits - 1))}>-</button>
            <input type="number" className="border rounded px-2 py-1 w-20 text-center" value={coolingUnits} onChange={e => setCoolingUnits(parseInt(e.target.value) || 0)} />
            <button className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded" onClick={() => setCoolingUnits(coolingUnits + 1)}>+</button>
          </div>
        </div>
        <button 
          onClick={handleRun} 
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors disabled:opacity-50"
        >
          {isLoading ? 'Computing...' : 'Run Allocation'}
        </button>
        {error && <p className="text-red-500 text-sm">{error.message}</p>}
      </div>

      {result && (
        <div className="flex-1 pb-8">
          <AllocationChart data={result} />
          
          <h4 className="font-semibold mt-8 mb-4">Top Allocations</h4>
          <div className="space-y-3">
            {result.optimizer.allocations.map(alloc => (
              <div key={alloc.block_id} className="border rounded p-3 bg-gray-50 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h5 className="font-medium text-gray-900">{alloc.block_name}</h5>
                    <span className="text-xs text-gray-500">{alloc.district}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold text-blue-600">{alloc.tankers} Tankers</div>
                    <div className="text-sm font-semibold text-orange-600">{alloc.cooling_units} Cooling</div>
                  </div>
                </div>
                <div className="text-xs text-gray-700 mb-1">
                  <strong>WHY BLOCK?</strong> Need: {formatNumber(alloc.need_score)} | Population: {formatNumber(alloc.population, 0)}
                </div>
                <p className="text-xs text-gray-500 italic">{alloc.rationale}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
