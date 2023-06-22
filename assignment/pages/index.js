import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
const ChartComponent = dynamic(() => import('./chart'), { ssr: false });

const IndexPage = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/data')
      .then(response => response.json())
      .then(data => {
        console.log('Response data:', data); // Log the response data

        if (Array.isArray(data)) {
          const modifiedData = data.map(item => {
            console.log('Original date:', item.time); // Log the original date
            const time = item.time && item.time.length >= 10 ? item.time.substring(0, 10) : '';
            const value = item.value || 0;
            return { time, value };
          });
          console.log('Modified data:', modifiedData); // Log the modified data
          setData(modifiedData);
        } else {
          console.error('Invalid response data:', data);
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h1>Optimism Number of Transaction per Day</h1>

      {data.length > 0 ? (
        <ChartComponent data={data} />
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
};

export default IndexPage;
