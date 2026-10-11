export function MapLegend({ activeLayer }: { activeLayer: string }) {
  const title = activeLayer.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <div className="absolute bottom-16 lg:bottom-6 right-3 sm:right-6 bg-white/95 backdrop-blur-md p-2.5 sm:p-3 rounded-xl shadow-md border border-gray-200/80 z-10 w-44 sm:w-56 pointer-events-auto">
      <h4 className="text-xs sm:text-sm font-semibold mb-1.5 text-gray-800">{title}</h4>
      <div className="flex h-2.5 sm:h-3 rounded-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 mb-1 shadow-inner" />
      <div className="flex justify-between text-[10px] sm:text-xs text-gray-600 font-medium">
        <span>Low</span>
        <span>Very High</span>
      </div>
    </div>
  );
}
