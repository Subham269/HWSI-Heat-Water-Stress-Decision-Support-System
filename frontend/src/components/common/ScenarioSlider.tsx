import * as Slider from '@radix-ui/react-slider';

interface ScenarioSliderProps {
  value: number;
  onChange: (val: number) => void;
}

export function ScenarioSlider({ value, onChange }: ScenarioSliderProps) {
  return (
    <div className="flex items-center gap-4">
      <span className="text-sm font-medium w-32">Scenario: +{value} days</span>
      <Slider.Root
        className="relative flex items-center select-none touch-none w-48 h-5"
        value={[value]}
        max={2}
        step={1}
        onValueChange={(vals) => onChange(vals[0])}
      >
        <Slider.Track className="bg-gray-200 relative grow rounded-full h-2">
          <Slider.Range className="absolute bg-blue-500 rounded-full h-full" />
        </Slider.Track>
        <Slider.Thumb
          className="block w-5 h-5 bg-white border-2 border-blue-500 shadow-md rounded-full hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-400"
          aria-label="Scenario days"
        />
      </Slider.Root>
    </div>
  );
}
