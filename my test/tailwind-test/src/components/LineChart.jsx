import React, { PureComponent, useState, useEffect, useContext } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

import { useGetData, QueryDataResultContext } from './providers/QuerysManager'
import { useTimelapse } from './providers/SidebarContext'
import { useExportData } from './providers/SidebarContext';
import { useDevServSelected } from './providers/SidebarContext';
import { usePackagedData } from './providers/SidebarContext';
import { useDate } from './providers/SidebarContext';
import { useDataFilter } from './providers/SidebarContext';
import { useShift } from './providers/SidebarContext'



export default function LineGraph() {
    const { timelapse, updateTimelapse } = useTimelapse();
    const { isLoading, incomingData } = useGetData();
    const { dataFilter, updateDataFilter } = useDataFilter();
    const contextData = useContext(QueryDataResultContext);
    const { devServSelected, updateDevServSelected } = useDevServSelected();
    const { selectedDate } = useDate();
    const { shift, updateShift } = useShift();
    const { dataToExport, dataToexportToCSV, updateExportData  } = useExportData();
    const {packagedData, updatePackagedData} = usePackagedData();
    const handlePackagedData = (name) =>{
        updatePackagedData(name);
    }

    let csvData = []
    useEffect(() => {handlePackagedData(csvData);}, [csvData]); // This will ensure it's called when csvData changes

    if(!selectedDate){
        return (<span className="text-white text-2xl font-bold  justify-left px-20 py-10 ">Por favor selecciona la fecha</span> )
    }
    if(!devServSelected){
        return (<span className="text-white text-2xl font-bold  justify-left px-20 py-10 ">Por favor selecciona el dispositivo o servicio</span> )
    }

    let incoming_data = incomingData?.data;
    if (incomingData?.data && Array.isArray(incomingData.data) && incomingData.data.length > 0) {
        incoming_data = incomingData.data
    }
    else { return (<span className="text-white text-2xl font-bold  justify-left px-20 py-10 ">Ooops... aún no se han generado datos para los filtros seleccionados</span> )}

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
    let periodicityLabelExportData = '';
    switch (timelapse) {
        case 'daily':
            periodicity = [...hours];
            periodicityLabel = 'Hora'
            periodicityLabelExportData = 'Diario'
            break;
        case 'weekly':
            periodicity = [...days];
            periodicityLabel = 'Dia'
            periodicityLabelExportData = 'Semanal'
            break;
        case 'monthly':
            periodicity = [...weeks];
            periodicityLabel = 'Semana'
            periodicityLabelExportData = 'Mensual'
            break;
        case 'yearly':
            periodicity = [...months]
            periodicityLabel = 'Mes'
            periodicityLabelExportData = 'Anual'
            break;
        default:
            periodicity = []
            break;
    }

    //////////////////////////////////////////////////////
    let devOrServ = '';
    switch(dataFilter){
        case 'devices':
            devOrServ = 'Dispositivo'
            break;
        case 'services':
            devOrServ = 'Servicio'
            break;
        default:
            devOrServ = 'error'
            break;
    }
    let exportShift = ''
    switch(shift){
        case 'day':
            exportShift = 'Diurno'
            break;
        case 'nigth':
            exportShift = 'Nocturno'
            break;
        default:
            exportShift = 'error'
            break;
    }

    const allGraphData = [];
    let currentIndex = 0;
    const exportDate = selectedDate.day.toString() + '/' + selectedDate.month.toString() + '/' + selectedDate.year.toString();


    // Add the title at the very beginning of the CSV data
    allGraphData.push([[devOrServ, devServSelected], ['Periodicidad', periodicityLabelExportData], ['Turno', exportShift], ['Fecha', exportDate]]);
    
    propertyArrays.forEach((property, index) => {
      const { prop, values } = property;
      const graphName = uniquePropsNames[index];
    
      const data = hours.map((time, hourIndex) => [
        `${periodicityLabel} ${time}`,
        values[hourIndex],
      ]);
    
      if (index === currentIndex) {
        // Append the graph name as the title only once for each graph
        data.unshift([`${graphName}`]);
        currentIndex++;
      }
    
      allGraphData.push(data);
    });
    
    // Flatten the array of data tto export
    csvData = allGraphData.flat();
    

    return (
        <div className="place-items-center flex flex-col">
            {propertyArrays.map((property, index) => {
                const { prop, values } = property;
                const { names } = uniquePropsNames[index]


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
                                    <LineChart width={400} height={300} data={data} margin={{ top: 20, right: 10, left: -10, bottom: 0 }}>

                                        <CartesianGrid strokeDasharray="3 3" vertical={true} />
                                        <XAxis dataKey={"name"} />
                                        <YAxis />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey={prop} name={uniquePropsNames[index]} stroke="#8884d8" strokeWidth={2} activeDot={{ r: 8 }} legendType="none" />
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




