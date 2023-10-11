import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import Dashboard from '../Dashboard'
import Testbutton from './Testbutton'
import ExportTest from '../ExportTest';


import { DateProvider, TimelapseProvider } from '../providers/SidebarContext'
import { ShiftProvider } from '../providers/SidebarContext'
import { DataFilterProvider } from '../providers/SidebarContext'
import { DevServSelectedProvider } from '../providers/SidebarContext'
import { Dateselector } from '../providers/SidebarContext'
import { ExportDataProvider } from '../providers/SidebarContext';
import { PackagedDataProvider } from '../providers/SidebarContext';



const queryClient = new QueryClient();

export default function Layout() {
  return (
    <div className="flex flex-row h-screen w-screen overflow-hidden px-5 py-5 bg-hero_pattern bg-no-repeat bg-cover">
      <QueryClientProvider client={queryClient}>
        <TimelapseProvider><ShiftProvider><DataFilterProvider><DevServSelectedProvider><DateProvider><ExportDataProvider><PackagedDataProvider>
          <Sidebar />
          <div className='flex-1'>
            <Header />
            <Dashboard />
          </div>
          </PackagedDataProvider></ExportDataProvider></DateProvider></DevServSelectedProvider></DataFilterProvider></ShiftProvider></TimelapseProvider>
      </QueryClientProvider>
    </div>
  );
}



