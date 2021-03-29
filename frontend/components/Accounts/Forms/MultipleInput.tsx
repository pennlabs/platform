import { useState } from "react";
import styled from "styled-components";
import { useField, FieldArray } from "formik";

import {
  AddButton,
  Flex,
  Indicator,
  Tag,
  FormInput,
  Button,
  Text,
  Span,
} from "../ui";
import { useOnClickOutside } from "../../useOnClickOutside";

const Dropdown = styled.div<{ isVisible: boolean }>`
    position: absolute;
    left: 0rem;
    top: 1.2rem;
    border-radius: 0.2rem;
    box-shadow: 1px 1px 1px rgba(185, 185, 185, 0.32);
    display: ${(props) => (props.isVisible ? "flex" : "none")};
    flex-direction: column;
    z-index: 99;
    background-color: #ffffff;
    overflow: hidden;
`;

const DropdownItem = styled.div`
    align-items: center;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0.2rem;

    :hover {
        background-color: #eeeeee;
        cursor: pointer;
    }
`;

export const FormikMultipleInputs = ({ baseName, fieldName, addText }) => {
  const [showAdd, setShowAdd] = useState(true);
  return (
    <FieldArray name={baseName}>
      {({ form, push, remove }) => {
        const addField = () => {
          push({ [fieldName]: "" });
        };
        const delField = (index) => {
          remove(index);
        }
        return (
          <>
            {form.values[baseName].map(({ id }, index) => (
              <FieldInput
                index={index}
                key={id}
                baseName={baseName}
                fieldName={fieldName}
                onConfirm={() => {
                  setShowAdd(true);
                }}
                delField={delField}
              />
            ))}
            {showAdd && (
              <AddInput
                margin={
                  form.values[baseName].length === 0
                    ? "0.6rem"
                    : undefined
                }
                text={addText}
                onClick={() => {
                  addField();
                  setShowAdd(false);
                }}
              />
            )}
          </>
        );
      }}
    </FieldArray>
  );
};

const FieldInput = ({ index, baseName, fieldName, onConfirm, delField }) => {
  const [field, meta] = useField({
    name: `${baseName}[${index}][${fieldName}]`,
  });
  const [isEdit, setIsEdit] = useState(field.value.length === 0);

  if (isEdit) {
    return (
      <EditInput
        {...field}
        onConfirm={() => {
          onConfirm();
          setIsEdit(false);
        }}
      />
    );
  } else {
    return <ExistingInput text={field.value} onDelete={() => delField(index)} />;
  }
};

const MoreIndicator = ({ onDelete }) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useOnClickOutside(() => setIsVisible(false), !isVisible);
  return (
    <>
      <Span position="relative">
        <Indicator src="/more.svg" onClick={() => setIsVisible(true)} />
        <Dropdown ref={ref as any} isVisible={isVisible}>
          <DropdownItem>
            <Text weight="400" size="0.7rem">
              Set primary
                        </Text>
          </DropdownItem>
          <DropdownItem onClick={onDelete}>
            <Text weight="400" size="0.7rem">
              Remove
                        </Text>
          </DropdownItem>
        </Dropdown>
      </Span>
    </>
  );
};

export const ExistingInput = ({ text, onDelete }) => {
  return (
    <Flex childMargin="0.2rem">
      <Indicator src="/greentick.png" />
      <span>{text}</span>
      <Tag>
        <span>PRIMARY</span>
      </Tag>
      <MoreIndicator onDelete={onDelete} />
    </Flex>
  );
};

export const AddInput = ({ text, onClick, margin }) => {
  return (
    <AddButton onClick={onClick} marginTop={margin}>
      {text}
    </AddButton>
  );
};

export const EditInput = ({ onConfirm, ...field }) => {
  return (
    <Flex childMargin="0.2rem" width="100%">
      <FormInput height="2rem" {...field} />
      <Button onClick={onConfirm}>Confirm</Button>
    </Flex>
  );
};
