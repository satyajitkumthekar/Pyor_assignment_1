import { useEffect, useRef } from 'react';
import { createChart, CrosshairMode } from 'lightweight-charts';

const Chart = ({ data }) => {
  const chartContainerRef = useRef(null);

  useEffect(() => {
    if (data && chartContainerRef.current) {
      const chartOptions = {
        layout: {
          textColor: 'black',
          backgroundColor: 'white',
        },
        crosshair: {
          mode: CrosshairMode.Normal,
        },
      };

      const chart = createChart(chartContainerRef.current, chartOptions);
      const areaSeries = chart.addAreaSeries();

      areaSeries.setData(data);
      chart.timeScale().fitContent();
    }
  }, [data]);

  return <div ref={chartContainerRef} style={{ height: '400px' }} />;
};

export default Chart;
