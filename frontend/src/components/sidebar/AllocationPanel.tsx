import { useState } from 'react';
import { useAllocation } from '@/hooks/useAllocation';
import { AllocationChart } from '@/components/charts/AllocationChart';
import { formatNumber } from '@/lib/utils';
import { Truck, Sun, Sparkles, Layers } from 'lucide-react';

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

  const priorityAllocations = result?.optimizer.allocations.filter(
    alloc => alloc.tankers > 0 || alloc.cooling_units > 0
  ) || [];

  return (
    <div className="p-3 sm:p-5 flex flex-col h-full overflow-y-auto">
      {/* Header */}
      <div className="mb-4">
        <h3 className="text-lg font-bold text-gray-900 tracking-tight">Resource Allocation</h3>
        <p className="text-xs text-gray-500 mt-0.5 text-pretty">
          Configure available emergency resources and compute optimal integer distribution via marginal benefit.
        </p>
      </div>

      {/* Resource Inputs Card */}
      <div className="bg-gray-50/90 border border-gray-200/90 rounded-xl p-3 sm:p-4 mb-5 shadow-2xs space-y-3">
        <div className="space-y-2.5">
          {/* Water Tankers Input */}
          <div className="bg-white p-2.5 sm:p-3 rounded-lg border border-gray-200 shadow-2xs flex items-center justify-between gap-3">
            <div className="min-w-0 pr-1">
              <div className="flex items-center gap-1.5">
                <Truck className="w-4 h-4 text-blue-600 shrink-0" />
                <label className="text-xs font-bold text-gray-800">Water Tankers</label>
              </div>
              <p className="text-[11px] text-gray-500 mt-0.5 truncate">Potable water logistics</p>
            </div>
            
            <div className="flex items-center gap-1 shrink-0">
              <button 
                type="button"
                className="w-7 h-7 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md border border-gray-200/60 transition-all touch-manipulation select-none" 
                onClick={() => setTankers(Math.max(0, tankers - 1))}
                aria-label="Decrease tankers"
              >
                -
              </button>
              <input 
                type="number" 
                min="0"
                max="500"
                className="w-12 h-7 border border-gray-200 rounded-md text-center font-bold text-gray-800 text-xs tabular-nums focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white" 
                value={tankers} 
                onChange={e => setTankers(Math.max(0, parseInt(e.target.value) || 0))} 
              />
              <button 
                type="button"
                className="w-7 h-7 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md border border-gray-200/60 transition-all touch-manipulation select-none" 
                onClick={() => setTankers(tankers + 1)}
                aria-label="Increase tankers"
              >
                +
              </button>
            </div>
          </div>

          {/* Cooling/ORS Units Input */}
          <div className="bg-white p-2.5 sm:p-3 rounded-lg border border-gray-200 shadow-2xs flex items-center justify-between gap-3">
            <div className="min-w-0 pr-1">
              <div className="flex items-center gap-1.5">
                <Sun className="w-4 h-4 text-amber-600 shrink-0" />
                <label className="text-xs font-bold text-gray-800">Cooling / ORS Shelters</label>
              </div>
              <p className="text-[11px] text-gray-500 mt-0.5 truncate">Hydration & cooling shelters</p>
            </div>
            
            <div className="flex items-center gap-1 shrink-0">
              <button 
                type="button"
                className="w-7 h-7 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md border border-gray-200/60 transition-all touch-manipulation select-none" 
                onClick={() => setCoolingUnits(Math.max(0, coolingUnits - 1))}
                aria-label="Decrease cooling units"
              >
                -
              </button>
              <input 
                type="number" 
                min="0"
                max="500"
                className="w-12 h-7 border border-gray-200 rounded-md text-center font-bold text-gray-800 text-xs tabular-nums focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white" 
                value={coolingUnits} 
                onChange={e => setCoolingUnits(Math.max(0, parseInt(e.target.value) || 0))} 
              />
              <button 
                type="button"
                className="w-7 h-7 flex items-center justify-center font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 active:scale-95 rounded-md border border-gray-200/60 transition-all touch-manipulation select-none" 
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
          className="w-full bg-blue-600 hover:bg-blue-700 active:scale-[0.99] text-white font-semibold py-2.5 px-4 rounded-lg shadow-sm transition-all disabled:opacity-50 text-xs sm:text-sm flex items-center justify-center gap-2 touch-manipulation"
        >
          {isLoading ? (
            <>
              <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Optimizing Allocation...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Run Allocation Optimization</span>
            </>
          )}
        </button>
        {error && <p className="text-red-600 text-xs mt-1 text-center font-medium">{error.message}</p>}
      </div>

      {/* Results Section */}
      {result && (
        <div className="flex-1 pb-8 space-y-5">
          {/* Chart Card */}
          <div className="bg-white border border-gray-200/90 rounded-xl p-3.5 sm:p-4 shadow-2xs">
            <AllocationChart data={result} />
          </div>
          
          {/* Priority Allocations */}
          <div>
            <div className="flex items-center justify-between gap-2 mb-2.5">
              <h4 className="font-bold text-xs text-gray-900 uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                <span>Priority Block Allocations</span>
              </h4>
              <span className="text-[11px] font-semibold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                {priorityAllocations.length} Blocks
              </span>
            </div>

            <div className="space-y-2.5">
              {result.optimizer.allocations.map(alloc => (
                <div 
                  key={alloc.block_id} 
                  className="border border-gray-200/90 rounded-xl p-3 bg-white shadow-2xs hover:border-blue-300 hover:shadow-xs transition-all"
                >
                  <div className="flex items-start justify-between gap-2 mb-1.5">
                    <div className="min-w-0 pr-1">
                      <h5 className="font-bold text-gray-900 text-sm leading-tight truncate">
                        {alloc.block_name}
                      </h5>
                      <span className="text-[11px] text-gray-500 font-medium">
                        {alloc.district} District
                      </span>
                    </div>

                    <div className="flex flex-wrap items-center justify-end gap-1 shrink-0">
                      {alloc.tankers > 0 && (
                        <span className="px-1.5 py-0.5 text-[11px] font-bold rounded-md bg-blue-50 text-blue-700 border border-blue-200/80 tabular-nums">
                          {alloc.tankers} Tanker{alloc.tankers > 1 ? 's' : ''}
                        </span>
                      )}
                      {alloc.cooling_units > 0 && (
                        <span className="px-1.5 py-0.5 text-[11px] font-bold rounded-md bg-amber-50 text-amber-700 border border-amber-200/80 tabular-nums">
                          {alloc.cooling_units} Cooling
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="text-[11px] text-gray-600 mb-2 flex items-center justify-between pt-1 border-t border-gray-100">
                    <span>Need Score: <strong className="text-gray-900 font-mono">{formatNumber(alloc.need_score, 3)}</strong></span>
                    <span>Population: <strong className="text-gray-900 font-mono">{formatNumber(alloc.population, 0)}</strong></span>
                  </div>

                  <p className="text-[11px] text-gray-600 leading-relaxed bg-gray-50/80 rounded-lg p-2 border border-gray-100 text-pretty">
                    {alloc.rationale}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
