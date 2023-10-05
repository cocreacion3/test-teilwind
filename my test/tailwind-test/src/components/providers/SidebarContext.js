import React, { createContext, useContext, useState } from 'react';


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

const ShaftContext = createContext();

export function ShaftProvider({ children }) {
  const [shaft, setShaft] = useState('day');

  const updateShaft = (newShaft) => {
    setShaft(newShaft);
  }

  return (
    <ShaftContext.Provider value={{ shaft, updateShaft }}>
      {children}
    </ShaftContext.Provider>
  )
}

export function useShaft() {
  const context = useContext(ShaftContext);
  if (!context) {
    throw new Error('useShaft must be used within a ShaftProvider');
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