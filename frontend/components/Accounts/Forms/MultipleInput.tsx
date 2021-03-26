import { useState } from "react";
import styled from "styled-components";

import { AddButton, Flex, Indicator, Tag, FormInput, Button, Text } from "../ui";
import { useOnClickOutside } from "../../useOnClickOutside";

const Dropdown = styled.div<{ isVisible: boolean }>`
  position: absolute;
  left: 11.8rem;
  top: 1.5rem;
  border-radius: 0.2rem;
  box-shadow: 1px 1px 1px rgba(185, 185, 185, 0.32);
  display: ${(props) => props.isVisible ? "flex" : "none"};
  flex-direction: column;
  z-index: 99;
  background-color: #FFFFFF;
  overflow: hidden;
`;


const DropdownItem = styled.div`
  align-items: center;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-bottom: 0.2rem;

  :hover {
    background-color: #EEEEEE;
    cursor: pointer;
  }
`;


const MoreIndicator = () => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useOnClickOutside(() => setIsVisible(false), !isVisible);
  return (
    <>
      <Indicator src="/more.svg" onClick={() => setIsVisible(true)} />
      <Dropdown ref={ref as any} isVisible={isVisible}>
        <DropdownItem>
          <Text weight="400" size="0.7rem" >
            Set primary
          </Text>
        </DropdownItem>
        <DropdownItem>
          <Text weight="400" size="0.7rem" >
            Remove
          </Text>
        </DropdownItem>
      </Dropdown>
    </>
  )
}


export const ExistingInput = ({ text }) => {
  return (
    <Flex childMargin="0.2rem" position="relative">
      <Indicator src="/greentick.png" />
      <span>{text}</span>
      <Tag>
        <span>PRIMARY</span>
      </Tag>
      <MoreIndicator />
    </Flex>
  )
}

export const AddInput = ({ text }) => {
  return (
    <AddButton>
      {text}
    </AddButton>
  )
}

export const EditInput = () => {
  return (
    <Flex childMargin="0.2rem" width="100%">
      <FormInput height="2rem" />
      <Button>
        Confirm
      </Button>
    </Flex>
  )
}
