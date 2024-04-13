import React, { useState } from "react";
import tw from "tailwind-styled-components";

interface CurrentEnvProps {
  data: any;
}

const CurrentEnv: React.FC<CurrentEnvProps> = ({ data }) => {
  const [agentName, setAgentName] = useState<string>("mini-agi");
  const [reportLocation, setReportLocation] = useState<string>("./reports/mini-agi");
  const [openAiKey, setOpenAiKey] = useState<string>("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // handle form submission here
  };

  return (
    <CurrentEnvContainer>
      <Title>Env Variables</Title>
      <Form onSubmit={handleSubmit}>
        <EnvWrapper>
          <EnvLabel htmlFor="agent-name">Agent Name</EnvLabel>
          <EnvInput
            id="agent-name"
            value={agentName}
            onChange={(e) => setAgentName(e.target.value)}
            placeholder="mini-agi"
            required
          />
        </EnvWrapper>
        <EnvWrapper>
          <EnvLabel htmlFor="report-location">Report Location</EnvLabel>
          <EnvInput
            id="report-location"
            value={reportLocation}
            onChange={(e) => setReportLocation(e.target.value)}
            placeholder="Location from root"
            required
          />
        </EnvWrapper>
        <EnvWrapper>
          <EnvLabel htmlFor="open-ai-key">OpenAI Key</EnvLabel>
          <EnvInput
            id="open-ai-key"
            type="password"
            value={openAiKey
