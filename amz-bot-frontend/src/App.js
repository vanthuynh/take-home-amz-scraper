import React, { useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const App = () => {
  const [data, setData] = useState([]);
  const [fileSelected, setFileSelected] = useState(false);

  // const handleFileChange = (event) => {
  //   const file = event.target.files[0];
  //   const reader = new FileReader();

  //   reader.onload = (e) => {
  //     const contents = e.target.result;
  //     const csvHeader = contents.slice(0, contents.indexOf("\n")).split(",");
  //     console.log(csvHeader)
  //     const csvRows = contents.slice(contents.indexOf("\n") + 1).split("\n");
  //     console.log(csvRows)

  //     const array = csvRows.map(i => {
  //       const values = i.split(",");
  //       const obj = csvHeader.reduce((object, header, index) => {
  //         object[header] = values[index];
  //         return object;
  //       }, {});
  //       return obj;
  //     });

  //     setData(array);
  //   };

  //   if (file) {
  //     reader.readAsText(file);
  //     setFileSelected(true);
  //   }
  // };
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      const contents = e.target.result;
      const lines = contents.split("\n");   // retrieve first header row
      const header = lines[0].split(",");   // got all the headers
      const parsedData = [];
      var regex = /("[^"]+"|[^,]+)*/g;
      for (let i = 1; i < lines.length; i++) {
        var line = [lines[i]].map(function(lineStr) {
          return lineStr.split(regex);
        });
        const item = {};

        for (let j = 0, x = 1; j < header.length; j++, x += 2) {
          const key = header[j].trim();
          // console.log(line[0][x])
          const value = line[0][x];

          item[key] = value;
        }

        parsedData.push(item);
      }

      setData(parsedData);
    };

    if (file) {
      reader.readAsText(file);
      setFileSelected(true);
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />

      {!fileSelected && <p>Please select a file.</p>}

      {data.length > 0 && (
        <div className="charts-container">
          <div className="chart">
            <LineChart
              width={500}
              height={300}
              data={data}
              margin={{
                top: 5,
                right: 30,
                left: 0,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Category" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="Value"
                stroke="#F94141"
                strokeWidth="3"
              />
            </LineChart>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
