import * as Slider from '@radix-ui/react-slider';

interface ScenarioSliderProps {
  value: number;
  onChange: (val: number) => void;
}

export function ScenarioSlider({ value, onChange }: ScenarioSliderProps) {
  return (
    <div className="flex items-center gap-2 sm:gap-3">
      <span className="text-xs sm:text-sm font-medium text-gray-700 whitespace-nowrap">
        <span className="hidden xs:inline">Scenario: </span>
        <span className="font-semibold text-blue-600">+{value}d</span>
      </span>
      <Slider.Root
        className="relative flex items-center select-none touch-none w-24 sm:w-36 md:w-44 h-5"
        value={[value]}
        max={2}
        step={1}
        onValueChange={(vals) => onChange(vals[0])}
        aria-label="Scenario forecast days"
      >
        <Slider.Track className="bg-gray-200 relative grow rounded-full h-1.5 sm:h-2">
          <Slider.Range className="absolute bg-blue-600 rounded-full h-full" />
        </Slider.Track>
        <Slider.Thumb
          className="block w-4 h-4 sm:w-5 sm:h-5 bg-white border-2 border-blue-600 shadow-md rounded-full hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-1 transition-transform active:scale-110"
          aria-label="Scenario days"
        />
      </Slider.Root>
    </div>
  );
}
