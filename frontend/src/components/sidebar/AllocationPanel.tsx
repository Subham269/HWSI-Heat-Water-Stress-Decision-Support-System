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
    <div className="p-3 sm:p-5 flex flex-col h-full overflow-y-auto">
      <div className="mb-4">
        <h3 className="text-lg sm:text-xl font-bold text-gray-900 tracking-tight">Resource Allocation</h3>
        <p className="text-xs sm:text-sm text-gray-500 mt-0.5 text-pretty">
          Configure available emergency resources and compute optimal integer distribution.
        </p>
      </div>

      <div className="bg-gray-50/80 border border-gray-200/80 rounded-xl p-3 sm:p-4 mb-6 shadow-sm space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          {/* Water Tankers Input */}
          <div className="bg-white p-2.5 rounded-lg border border-gray-200 shadow-2xs">
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">Water Tankers</label>
            <div className="flex items-center gap-1.5">
              <button 
                type="button"
                className="w-8 h-8 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md transition-all touch-manipulation" 
                onClick={() => setTankers(Math.max(0, tankers - 1))}
                aria-label="Decrease tankers"
              >
                -
              </button>
              <input 
                type="number" 
                className="border border-gray-200 rounded-md h-8 flex-1 text-center font-bold text-gray-800 text-sm tabular-nums focus:outline-none focus:ring-2 focus:ring-blue-500" 
                value={tankers} 
                onChange={e => setTankers(parseInt(e.target.value) || 0)} 
              />
              <button 
                type="button"
                className="w-8 h-8 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md transition-all touch-manipulation" 
                onClick={() => setTankers(tankers + 1)}
                aria-label="Increase tankers"
              >
                +
              </button>
            </div>
          </div>

          {/* Cooling/ORS Units Input */}
          <div className="bg-white p-2.5 rounded-lg border border-gray-200 shadow-2xs">
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">Cooling / ORS Shelters</label>
            <div className="flex items-center gap-1.5">
              <button 
                type="button"
                className="w-8 h-8 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md transition-all touch-manipulation" 
                onClick={() => setCoolingUnits(Math.max(0, coolingUnits - 1))}
                aria-label="Decrease cooling units"
              >
                -
              </button>
              <input 
                type="number" 
                className="border border-gray-200 rounded-md h-8 flex-1 text-center font-bold text-gray-800 text-sm tabular-nums focus:outline-none focus:ring-2 focus:ring-blue-500" 
                value={coolingUnits} 
                onChange={e => setCoolingUnits(parseInt(e.target.value) || 0)} 
              />
              <button 
                type="button"
                className="w-8 h-8 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md transition-all touch-manipulation" 
                onClick={() => setCoolingUnits(coolingUnits + 1)}
                aria-label="Increase cooling units"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <button 
          onClick={handleRun} 
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 active:scale-[0.99] text-white font-medium py-2.5 px-4 rounded-lg shadow-sm transition-all disabled:opacity-50 text-sm flex items-center justify-center gap-2 touch-manipulation"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Optimizing Allocation...</span>
            </>
          ) : (
            'Run Allocation'
          )}
        </button>
        {error && <p className="text-red-600 text-xs mt-1 text-center">{error.message}</p>}
      </div>

      {result && (
        <div className="flex-1 pb-8 space-y-6">
          <div className="bg-white border border-gray-200 rounded-xl p-3 sm:p-4 shadow-sm">
            <AllocationChart data={result} />
          </div>
          
          <div>
            <h4 className="font-bold text-sm text-gray-900 mb-3 uppercase tracking-wider">Top Priority Block Allocations</h4>
            <div className="space-y-2.5">
              {result.optimizer.allocations.map(alloc => (
                <div key={alloc.block_id} className="border border-gray-200 rounded-lg p-3 bg-white shadow-2xs hover:border-gray-300 transition-colors">
                  <div className="flex justify-between items-start gap-2 mb-1.5">
                    <div>
                      <h5 className="font-semibold text-gray-900 text-sm">{alloc.block_name}</h5>
                      <span className="text-xs text-gray-500">{alloc.district} District</span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      {alloc.tankers > 0 && (
                        <span className="px-2 py-0.5 text-xs font-bold rounded-md bg-blue-50 text-blue-700 border border-blue-200">
                          {alloc.tankers} Tankers
                        </span>
                      )}
                      {alloc.cooling_units > 0 && (
                        <span className="px-2 py-0.5 text-xs font-bold rounded-md bg-amber-50 text-amber-700 border border-amber-200">
                          {alloc.cooling_units} Cooling
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 mb-1 flex items-center gap-3">
                    <span>Need Score: <strong className="text-gray-900 font-mono">{formatNumber(alloc.need_score, 3)}</strong></span>
                    <span>Pop: <strong className="text-gray-900 font-mono">{formatNumber(alloc.population, 0)}</strong></span>
                  </div>
                  <p className="text-[11px] text-gray-500 italic bg-gray-50 rounded p-1.5 border border-gray-100">{alloc.rationale}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
