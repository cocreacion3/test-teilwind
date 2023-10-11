import React, { createContext, useContext } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

import { useTimelapse } from '../providers/SidebarContext'
import { useShift } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';
import { useDate } from '../providers/SidebarContext';




//////////////////////////////////////////////////////////////// query list of devices or services
export const QueryDevServResultContext = createContext();

export function useGetList(listType) {
  let query = '';
  if (listType === 'services') {
    // console.log('en services');
    query = `http://127.0.0.1:3001/query_services`;
  } else if (listType === 'devices') {
    // console.log('en devices');
    query = `http://127.0.0.1:3001/query_devices`;
  }

  const { isLoading: isLoadingListItems, data: incomingDataListItems } = useQuery(
    ['getListItems', listType],
    () => {
      return axios.get(query);
    }
  );

  return { isLoadingListItems, incomingDataListItems };
}

////////////////////////////////////////////////////////////////Data query

export const QueryDataResultContext = createContext();

export function useGetData() {
  const { timelapse, updateTimelapse } = useTimelapse();
  const { shift, updateShift } = useShift();
  const { dataFilter, updateDataFilter } = useDataFilter();
  const { devServSelected, updateDevServSelected } = useDevServSelected();
  const { selectedDate } = useDate();
 
  let query = '';
  if (dataFilter === 'devices') {
    query = 'http://127.0.0.1:3001/data_devices?';
  } else if (dataFilter === 'services') {
    query = 'http://127.0.0.1:3001/data_services?';
  }

  const { isLoading, data: incomingData } = useQuery(
    ['getData', timelapse, shift, dataFilter, devServSelected, selectedDate],
    () => {
      // Construct the query parameters
      const params = new URLSearchParams({
        item: devServSelected,
        periodicity: timelapse,
        shift: shift,
        day: selectedDate.day,
        month: selectedDate.month,
        year: selectedDate.year,
      });

      // Log the query URL for debugging
      console.log('Query URL: ', `${query}${params}`);

      // Make the network request using Axios or your preferred library
      return axios.get(`${query}${params}`);
    },
    {
      enabled:
        timelapse !== undefined &&
        shift !== undefined &&
        dataFilter !== undefined &&
        devServSelected !== undefined &&
        selectedDate !== undefined,
    }
  );
  return { isLoading, incomingData };
}
