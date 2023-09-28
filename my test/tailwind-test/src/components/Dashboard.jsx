import React from 'react'
import LineChart from './LineChart'

export default function Dashboard() {
  return (
    <div className=" overflow-y-auto h-5/6">
      <LineChart />
      <LineChart />
      <LineChart />
    </div>

  )
}
