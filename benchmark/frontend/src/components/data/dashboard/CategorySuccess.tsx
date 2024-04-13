import React, { ReactNode, useState } from "react";
import tw from "tailwind-styled-components";

interface CategorySuccessProps {
  data: {
    id: number;
    name: string;
  };
}

const CategorySuccessContainer = tw.div`
  p-4
  bg-green-200
  text-green-800
  font-semibold
  rounded-lg
  shadow-md
`;

const CategorySuccess: React.FC<CategorySuccessProps> = ({ data }) => {
  return <CategorySuccessContainer key={data.id}>{data.name}</CategorySuccessContainer>;
};

export default CategorySuccess;
