export function MapLegend({ activeLayer }: { activeLayer: string }) {
  const title = activeLayer.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <div className="absolute bottom-6 right-6 bg-white p-4 rounded shadow-md border z-10 w-64">
      <h4 className="text-sm font-semibold mb-2">{title}</h4>
      <div className="flex h-3 rounded bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 mb-1" />
      <div className="flex justify-between text-xs text-gray-600">
        <span>Low</span>
        <span>Very High</span>
      </div>
    </div>
  );
}
