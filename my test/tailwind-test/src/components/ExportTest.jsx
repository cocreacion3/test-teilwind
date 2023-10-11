import React from 'react';
import Papa from 'papaparse';

const data = [0, 1, 2, 3, 4];

const exportToCSV = (data, fileName) => {
  // Convert the data to a two-dimensional array format
  const csvData = data.map(item => [item]);

  const csv = Papa.unparse(csvData);
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });

  if (window.navigator.msSaveBlob) {
    // For Internet Explorer
    window.navigator.msSaveBlob(blob, fileName);
  } else {
    // For other browsers
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = fileName;
    link.click();
    URL.revokeObjectURL(url);
  }
};

export default function ExportTest() {
  return (
    <button onClick={() => exportToCSV(data, 'exported_data.csv')}>Export to CSV</button>
  );
}