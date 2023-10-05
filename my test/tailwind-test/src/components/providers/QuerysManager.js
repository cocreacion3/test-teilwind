import React, { createContext, useContext } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

export const QueryDevServResultContext = createContext();

export function useGetList(listType) {
  let query = '';
  if (listType === 'services') {
    // console.log('en services');
    query = `http://127.0.0.1:5000/query_services`;
  } else if (listType === 'devices') {
    // console.log('en devices');
    query = `http://127.0.0.1:5000/query_devices`;
  }

  const { isLoading: isLoadingListItems, data: incomingDataListItems } = useQuery(
    ['getListItems', listType],
    () => {
      return axios.get(query);
    }
  );

  return { isLoadingListItems, incomingDataListItems };
}
