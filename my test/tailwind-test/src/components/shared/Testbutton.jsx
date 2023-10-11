import React, { useState, useEffect, useContext } from 'react'

import { useTimelapse } from '../providers/SidebarContext'
import { useShift } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';
import { useDate } from '../providers/SidebarContext';

import { useGetList, QueryDevServResultContext, useGetData } from '../providers/QuerysManager'
import { useDetData, QueryDataResultContext } from '../providers/QuerysManager'
import { useExportData } from '../providers/SidebarContext';
import { usePackagedData } from '../providers/SidebarContext';


export default function Testbutton() {
  const {packagedData, updatePackagedData} = usePackagedData();
  const { exportToCSV, exportedData } = useExportData();

      const handleExport = () => {
      exportToCSV(packagedData, 'all_graphs_data.csv');
    };

  return (
    <div>
      <div>
        <h2>Data:</h2>
        {/* <pre>{JSON.stringify(packagedData, null, 2)}</pre> */}
        <button onClick={handleExport}>Export All Graphs to CSV</button>
      </div>
    </div>
  );
}