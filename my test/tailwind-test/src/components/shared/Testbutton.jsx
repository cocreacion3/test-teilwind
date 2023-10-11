import React, { useState, useEffect, useContext } from 'react'

import { useTimelapse } from '../providers/SidebarContext'
import { useShift } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';
import { useDate } from '../providers/SidebarContext';

import { useGetList, QueryDevServResultContext, useGetData } from '../providers/QuerysManager'
import { useDetData, QueryDataResultContext } from '../providers/QuerysManager'


export default function Testbutton() {
  const { isLoading, incomingData } = useGetData();
  const contextData = useContext(QueryDataResultContext);
  let data = incomingData.data || [];

  console.log("Query data = ", data);

  return (
    <div>
      <div>
        <h2>Data:</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}