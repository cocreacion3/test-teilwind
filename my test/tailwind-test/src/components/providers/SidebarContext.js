import React, { createContext, useContext, useState } from 'react';
import Papa from 'papaparse';

////////////////////////////////////////////////Context Periodicity buttons
const TimelapseContext = createContext();

export function TimelapseProvider({ children }) {
  const [timelapse, setTimelapse] = useState('daily');

  const updateTimelapse = (newTimelapse) => {
    setTimelapse(newTimelapse);
  };

  return (
    <TimelapseContext.Provider value={{ timelapse, updateTimelapse }}>
      {children}
    </TimelapseContext.Provider>
  );
}

export function useTimelapse() {
  const context = useContext(TimelapseContext);
  if (!context) {
    throw new Error('useTimelapse must be used within a TimelapseProvider');
  }
  return context;
}
////////////////////////////////////////////////Context Shaft buttons

const ShiftContext = createContext();

export function ShiftProvider({ children }) {
  const [shift, setShift] = useState('day');

  const updateShift = (newShift) => {
    setShift(newShift);
  }

  return (
    <ShiftContext.Provider value={{ shift, updateShift }}>
      {children}
    </ShiftContext.Provider>
  )
}

export function useShift() {
  const context = useContext(ShiftContext);
  if (!context) {
    throw new Error('useShift must be used within a ShaftProvider');
  }
  return context;
}

////////////////////////////////////////////////Context Device/Service buttons
const DataFilterContext = createContext();

export function DataFilterProvider({ children}){
  const [dataFilter, setDataFilter] = useState('devices');

  const updateDataFilter =(newDataFilter) => {
    setDataFilter(newDataFilter);
  }

  return(
    <DataFilterContext.Provider value={{ dataFilter, updateDataFilter }}>
      {children}
      </DataFilterContext.Provider>
  )
}

export function useDataFilter() {
  const context = useContext(DataFilterContext);
  if (!context) {
    throw new Error('useDataFilter must be used within a DataFilterProvider');
  }
  return context;
}

////////////////////////////////////////////////Context Device/Service selected
const DevServSelectedContext = createContext();

export function DevServSelectedProvider({ children}){
  const [devServSelected, setDevServSelected] = useState();

  const updateDevServSelected =(selected) => {
    setDevServSelected(selected);
  }

  return(
    <DevServSelectedContext.Provider value={{ devServSelected, updateDevServSelected }}>
      {children}
      </DevServSelectedContext.Provider>
  )
}

export function useDevServSelected() {
  const context = useContext(DevServSelectedContext);
  if (!context) {
    throw new Error('useDevServSelected must be used within a DevServSelectedProvider');
  }
  
  return context;
}

////////////////////////////////////////////////Context for Date selected
const DateContext = createContext();

export const useDate = () => {
  return useContext(DateContext);
};

export const DateProvider = ({ children }) => {
  const [selectedDate, setSelectedDate] = useState(null);

  const setDate = (day, month, year) => {
    setSelectedDate({ day, month, year });
  };

  return (
    <DateContext.Provider value={{ selectedDate, setDate }}>
      {children}
    </DateContext.Provider>
  );
};

////////////////////////////////////////////////Context for the packaged data
const PackagedDataContext = createContext();

export function PackagedDataProvider({children}){
  const [packagedData, setPackagedData] = useState([]);

  const updatePackagedData = (data)=>{
    setPackagedData(data)
  }

  return(
    <PackagedDataContext.Provider value={{packagedData, updatePackagedData}}>
      {children}
    </PackagedDataContext.Provider>
  )
}

export function usePackagedData(){
  const context = useContext(PackagedDataContext);
  if (!context) {
    throw new Error('usePackagedData must be used within a PackagedDataProvider');
  }

  return context;
}
////////////////////////////////////////////////Context for export data
const ExportDataContext = createContext();

export function ExportDataProvider({ children }) {
  const [exportedData, setExportedData] = useState([]);

  const exportToCSV = (data, fileName) => {
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

    // Store the data that was exported
    setExportedData(csvData);
  };

  return (
    <ExportDataContext.Provider value={{ exportToCSV, exportedData }}>
      {children}
    </ExportDataContext.Provider>
  );
}

export function useExportData() {
  return useContext(ExportDataContext);
}