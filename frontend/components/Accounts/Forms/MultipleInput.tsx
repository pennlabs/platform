import { AddButton, Flex, Indicator, Tag, FormInput, Button } from "../ui";

export const ExistingInput = ({ text }) => {
  return (
    <Flex childMargin="0.2rem">
      <Indicator src="/greentick.png" />
      <span>{text}</span>
      <Tag>
        <span>PRIMARY</span>
      </Tag>
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
