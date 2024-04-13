import React, { useState } from "react";
import tw, { TwStyle, TwStyleAny } from "tailwind-styled-components";

import RadarChart from "./dashboard/RadarChart";
import CategorySuccess from "./dashboard/CategorySuccess";
import CurrentEnv from "./dashboard/CurrentEnv";

interface DashboardProps {
  data: any;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  return (
    <DashboardContainer>
      <CardWrapper>
        <RadarChart />
      </CardWrapper>
      <CardWrapper>
        <CategorySuccess />
      </CardWrapper>
      <CardWrapper>
        <CurrentEnv />
      </CardWrapper>
    </DashboardContainer>
  );
};

export default Dashboard;

// Define a type for the styled component
type DashboardContainerStyles = TwStyle & TwStyleAny;

// Create a styled component with the defined type
const DashboardContainer = tw.div<DashboardContainerStyles>(
  "w-full h-96 flex justify-between items-center",
  {
    // Add any additional styles here
  }
);

// Define a type for the styled component
type CardWrapperStyles = TwStyle & TwStyleAny;

// Create a styled component with the defined type
const CardWrapper = tw.div<CardWrapperStyles>(
  "w-full md:w-1/3 lg:w-1/4 h-72 rounded-xl shadow-lg border p-4",
  {
    // Add any additional styles here
  }
);
