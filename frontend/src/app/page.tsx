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

export default function Dashboard() {
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [activeLayer, setActiveLayer] = useState<string>('hwsi');
  const [extraDays, setExtraDays] = useState<number>(0);

  const { data: riskData, error: riskError, isLoading: riskLoading } = useRiskData(extraDays);
  const { explanation, isLoading: explainLoading } = useBlockExplain(selectedBlockId);

  return (
    <div className="flex flex-col h-full w-full bg-gray-50">
      {/* Top Bar */}
      <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0 shadow-sm z-20">
        <h1 className="font-bold text-xl text-gray-900 tracking-tight">HWSI: Heat-Water Stress Decision Support</h1>
        
        <div className="flex items-center gap-8">
          <ScenarioSlider value={extraDays} onChange={setExtraDays} />
          
          <div className="flex items-center gap-2 border-l pl-6">
            <span className="text-sm font-medium text-gray-600">Data Status:</span>
            <DataBadge type={riskError ? 'STALE' : riskLoading ? 'PERIODIC' : 'LIVE'} />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Map Section */}
        <section className="w-[65vw] h-full relative border-r border-gray-200 bg-gray-100">
          <RiskMap 
            activeLayer={activeLayer}
            riskData={riskData}
            selectedBlockId={selectedBlockId}
            onBlockSelect={setSelectedBlockId}
          />
          <LayerToggle activeLayer={activeLayer} onChange={setActiveLayer} />
          <MapLegend activeLayer={activeLayer} />
        </section>

        {/* Sidebar Section */}
        <aside className="w-[35vw] h-full bg-white flex flex-col z-10 shadow-xl">
          <SidebarTabs 
            explanation={explanation || null}
            isExplainLoading={explainLoading}
            extraDays={extraDays}
          />
        </aside>
      </div>
    </div>
  );
}
