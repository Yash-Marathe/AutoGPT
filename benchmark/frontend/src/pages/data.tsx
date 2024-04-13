import React, { useState, useEffect } from "react";
import tw from "tailwind-styled-components";

import Dashboard from "~/components/data/Dashboard";
import Reports from "~/components/data/Reports";

type DataType = {
  // add types for the data here
};

const DataPage: React.FC = () => {
  const [data, setData] = useState<DataType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);

  const getData = async () => {
    try {
      let url = `http://localhost:8000/data`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error("Error in fetch");
      }

      const responseData = await response.json();

      if (responseData.length > 0) {
        setData(responseData);
      }

      setLoading(false);
    } catch (error) {
      console.error("There was an error fetching the data", error);
      setError(true);
      setLoading(false);
    }
  };

  useEffect(() => {
    getData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching data</div>;
  }

  return (
    <PageContainer>
      <Dashboard data={
