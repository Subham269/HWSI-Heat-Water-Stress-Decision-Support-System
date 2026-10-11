'use client';

import { useState } from 'react';
import { RiskMap } from '@/components/map/RiskMap';
import { LayerToggle } from '@/components/map/LayerToggle';
import { MapLegend } from '@/components/map/MapLegend';
import { SidebarTabs } from '@/components/sidebar/SidebarTabs';
import { ScenarioSlider } from '@/components/common/ScenarioSlider';
import { DataBadge } from '@/components/common/DataBadge';
import { useRiskData } from '@/hooks/useRiskData';
import { useBlockExplain } from '@/hooks/useBlockExplain';
import { cn } from '@/lib/utils';
import { Map as MapIcon, SlidersHorizontal } from 'lucide-react';

export default function Dashboard() {
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [activeLayer, setActiveLayer] = useState<string>('hwsi');
  const [extraDays, setExtraDays] = useState<number>(0);
  const [mobileView, setMobileView] = useState<'map' | 'sidebar'>('map');

  const { data: riskData, error: riskError, isLoading: riskLoading } = useRiskData(extraDays);
  const { explanation, isLoading: explainLoading } = useBlockExplain(selectedBlockId, extraDays);

  const handleBlockSelect = (blockId: string | null) => {
    setSelectedBlockId(blockId);
    // On small screens, smoothly switch to the sidebar when a block is clicked
    if (blockId && typeof window !== 'undefined' && window.innerWidth < 1024) {
      setMobileView('sidebar');
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-gray-50">
      {/* Top Bar */}
      <header className="h-14 sm:h-16 bg-white border-b border-gray-200/80 flex items-center justify-between px-3 sm:px-6 shrink-0 shadow-2xs z-20">
        <div className="flex items-center gap-2 min-w-0 mr-2">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse shrink-0" />
          <h1 className="font-bold text-sm sm:text-base md:text-xl text-gray-900 tracking-tight truncate">
            Project Bhumi
            <span className="hidden sm:inline font-normal text-gray-300 mx-2">|</span>
            <span className="hidden sm:inline font-normal text-gray-600 text-xs sm:text-sm">HWSI Decision Support</span>
          </h1>
        </div>

        <div className="flex items-center gap-2 sm:gap-6 shrink-0">
          <ScenarioSlider value={extraDays} onChange={setExtraDays} />

          <div className="hidden sm:flex items-center gap-2 border-l border-gray-200 pl-4 sm:pl-6">
            <span className="text-xs font-medium text-gray-500 hidden md:inline">Data Status:</span>
            <DataBadge type={riskError ? 'STALE' : riskLoading ? 'PERIODIC' : 'LIVE'} />
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Map Section */}
        <section 
          className={cn(
            "h-full relative bg-gray-100 transition-all duration-200",
            // Desktop: flex-1
            "lg:flex-1 lg:block",
            // Mobile: toggle visibility based on mobileView
            mobileView === 'map' ? "w-full block" : "hidden lg:block"
          )}
        >
          <RiskMap
            activeLayer={activeLayer}
            riskData={riskData}
            selectedBlockId={selectedBlockId}
            onBlockSelect={handleBlockSelect}
          />
          <LayerToggle activeLayer={activeLayer} onChange={setActiveLayer} />
          <MapLegend activeLayer={activeLayer} />
        </section>

        {/* Sidebar Section */}
        <aside 
          className={cn(
            "h-full bg-white flex flex-col z-10 shadow-xl border-l border-gray-200/80 transition-all duration-200",
            // Desktop: fixed width
            "lg:w-[380px] xl:w-[440px] 2xl:w-[480px] lg:shrink-0 lg:flex",
            // Mobile: full width when active
            mobileView === 'sidebar' ? "w-full flex" : "hidden lg:flex"
          )}
        >
          <SidebarTabs
            explanation={explanation || null}
            isExplainLoading={explainLoading}
            extraDays={extraDays}
          />
        </aside>

        {/* Mobile Navigation Pill */}
        <nav 
          aria-label="Mobile View Toggle" 
          className="lg:hidden fixed bottom-4 left-1/2 -translate-x-1/2 z-30 bg-gray-900/90 backdrop-blur-md text-white p-1 rounded-full shadow-2xl border border-gray-700/80 flex gap-1 items-center"
        >
          <button
            onClick={() => setMobileView('map')}
            className={cn(
              "px-4 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all touch-manipulation",
              mobileView === 'map' ? "bg-blue-600 text-white shadow-sm" : "text-gray-300 hover:text-white"
            )}
          >
            <MapIcon className="w-3.5 h-3.5" />
            <span>Map View</span>
          </button>
          <button
            onClick={() => setMobileView('sidebar')}
            className={cn(
              "px-4 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all touch-manipulation relative",
              mobileView === 'sidebar' ? "bg-blue-600 text-white shadow-sm" : "text-gray-300 hover:text-white"
            )}
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>{selectedBlockId ? 'Block Analysis' : 'Allocation'}</span>
            {selectedBlockId && mobileView === 'map' && (
              <span className="w-2 h-2 rounded-full bg-amber-400 absolute top-1 right-1 animate-pulse" />
            )}
          </button>
        </nav>
      </div>
    </div>
  );
}
