import React, { useState } from "react";
import tw from "tailwind-styled-components";

interface ReportsProps {
  data: any[];
}

const Reports: React.FC<ReportsProps> = ({ data }) => {
  return (
    <ReportsContainer>
      <Table data={data} />
    </ReportsContainer>
  );
};

const ReportsContainer = tw.div`
  w-full
`;

interface TableProps {
  data: any[];
}

const Table: React.FC<TableProps> = ({ data }) => {
  return (
    <table className="w-full border shadow-lg rounded-xl">
      <TableHeader />
      <TableBody data={data} />
    </table>
  );
};

interface TableHeaderProps {
  // no props needed
}

const TableHeader: React.FC<TableHeaderProps> = () => {
  return (
    <thead className="bg-gray-200">
      <tr>
        <th className="px-4 py-2">Column 1</th>
        <th className="px-4 py-2">Column 2</th>
      </tr>
    </thead>
  );
};

interface TableBodyProps {
  data: any[];
}

const TableBody: React.FC<TableBodyProps> = ({ data }) => {
  return (
    <tbody>
      {data.map((item, index) => (
        <TableRow key={index} data={item} />
      ))}
    </tbody>
  );
};

interface TableRowProps
