import React, { PureComponent, useState, useEffect, useContext } from 'react';
// import React, { PureComponent } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// import { useGetList, QueryDevServResultContext} from './providers/QuerysManager'
import { useGetData, QueryDataResultContext } from './providers/QuerysManager'
import { useTimelapse } from './providers/SidebarContext'


export default function LineGraph() {
    const { timelapse, updateTimelapse } = useTimelapse();
    const { isLoading, incomingData } = useGetData();
    const contextData = useContext(QueryDataResultContext);
    // console.log(timelapse);
    if (!timelapse) {
        return <p>No data available for the graph timelapse.</p>;
    }

    let incoming_data = incomingData?.data;
    if (incomingData?.data && Array.isArray(incomingData.data)) {
        incoming_data = incomingData.data
    }
    else { return <p>No data available for the graph.</p>; }

    // console.log("Query data = ", incoming_data);
    const hours = [];
    const days = [];
    const weeks = [];
    const months = [];
    const years = [];

    const propertiesData = [];

    incoming_data.forEach((item) => {
        hours.push(item.hour);
        days.push(item.day);
        weeks.push(item.week);
        months.push(item.month);
        years.push(item.year);
        propertiesData.push(item.properties);
    });
    //   console.log(hours, days, weeks, months, years, propertiesData);

    const uniqueProps = new Set();
    let uniquePropsNames = new Set();
    propertiesData.forEach((properties) => {
        properties.forEach((property) => {
            uniqueProps.add(property.prop);
            uniquePropsNames.add(property.name);
        });
    });
    const uniquePropsArray = [...uniqueProps];
    uniquePropsNames = [...uniquePropsNames];
    // console.log(uniquePropsNames[0])

    let propertyArrays = {};
    incoming_data.forEach((item) => {
        item.properties.forEach((property) => {
            if (!propertyArrays[property.prop]) {
                propertyArrays[property.prop] = [];
            }
            propertyArrays[property.prop].push(property.value);
        });
    });
    // console.log(propertyArrays);
    propertyArrays = Object.entries(propertyArrays).map(([key, value]) => ({ prop: key, values: value }));
    console.log(propertyArrays);

    //   console.log(uniquePropsArray)
    //   console.log(uniquePropsNames)


    let periodicity = [];
    let periodicityLabel = '';
    switch (timelapse) {
        case 'daily':
            periodicity = [...hours];
            periodicityLabel = 'Hora'
            break;
        case 'weekly':
            periodicity = [...days];
            periodicityLabel = 'Dia'
            break;
        case 'monthly':
            periodicity = [...weeks];
            periodicityLabel = 'Semana'
            break;
        case 'yearly':
            periodicity = [...months]
            periodicityLabel = 'Mese'
            break;
        default:
            periodicity = []
    }


    return (
        <div className="place-items-center flex flex-col">
            {propertyArrays.map((property, index) => {
                const { prop, values } = property;
                const {names} = uniquePropsNames[index]


                // Format data for the LineChart using the common 'hours' array
                const data = hours.map((time, hourIndex) => ({
                    name: periodicityLabel + " " + time,
                    [prop]: values[hourIndex],
                }));

                return (
                    <div key={index} className="py-5 w-11/12 items-center text-center">
                        <strong className="text-white text-xm flex py-3 justify-center font-bold">{uniquePropsNames[index]}</strong>
                        <div className="h-[20rem] bg-white px-3 py-6 rounded-xl border-gray-200 flex w-full">
                            <div className="mt-3 flex-1 text-xs gap-5">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart width={400} height={300} data={data} margin={{top: 20, right: 10, left: -10, bottom: 0}}>
                                        
                                        <CartesianGrid strokeDasharray="3 3" vertical={true} />
                                        <XAxis dataKey={"name"} />
                                        <YAxis />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey={prop} name={uniquePropsNames[index]} stroke="#8884d8" strokeWidth={2} activeDot={{ r: 8 }} legendType="none"/>
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );

}




