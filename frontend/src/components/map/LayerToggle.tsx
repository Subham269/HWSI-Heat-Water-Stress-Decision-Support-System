import { cn } from '@/lib/utils';

interface LayerToggleProps {
  activeLayer: string;
  onChange: (layer: string) => void;
}

export function LayerToggle({ activeLayer, onChange }: LayerToggleProps) {
  const layers = [
    { id: 'hwsi', label: 'HWSI' },
    { id: 'heat_hazard', label: 'Heat Hazard' },
    { id: 'water_stress', label: 'Water Stress' },
    { id: 'e_score', label: 'Exposure' },
    { id: 'v_score', label: 'Vulnerability' }
  ];

  return (
    <div className="absolute top-3 left-3 sm:top-5 sm:left-5 max-w-[calc(100vw-24px)] sm:max-w-none overflow-x-auto scrollbar-none bg-white/95 backdrop-blur-md p-1 rounded-xl shadow-md border border-gray-200/80 z-10 flex gap-1 items-center">
      {layers.map(layer => (
        <button
          key={layer.id}
          onClick={() => onChange(layer.id)}
          className={cn(
            'px-2.5 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm font-medium rounded-lg whitespace-nowrap transition-all touch-manipulation',
            activeLayer === layer.id 
              ? 'bg-blue-600 text-white shadow-sm' 
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/80'
          )}
        >
          {layer.label}
        </button>
      ))}
    </div>
  );
}
