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
    <div className="absolute top-6 left-6 bg-white p-1 rounded shadow-md border z-10 flex gap-1">
      {layers.map(layer => (
        <button
          key={layer.id}
          onClick={() => onChange(layer.id)}
          className={cn(
            'px-3 py-1.5 text-sm font-medium rounded transition-colors',
            activeLayer === layer.id ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
          )}
        >
          {layer.label}
        </button>
      ))}
    </div>
  );
}
