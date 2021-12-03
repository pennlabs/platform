import { useState } from "react";
import styled from "styled-components";
import { useToasts } from "react-toast-notifications";
import { useResourceList } from "@pennlabs/rest-hooks";
import parsePhoneNumber from "libphonenumber-js";

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
import VerificationModal from "../Modals/Verification";
import DeleteModal from "../Modals/Delete";
import { useOnClickOutside } from "../../useOnClickOutside";
import { ContactInfo, ContactType } from "../../../types";
import {
    createContact,
    deleteContact,
    reverifyContact,
} from "../../../data-fetching/accounts";

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

const FieldInput = ({
    mutate,
    contactType,
    setShowAdd,
    setVerifyContact,
    setShowModal,
    onCancel,
}) => {
    const { addToast } = useToasts();
    const [text, setText] = useState("");

    const onChange = (e) => {
        setText(e.target.value);
    };

    const onConfirm = async () => {
        let res;

        try {
            let payload;

            if (contactType === ContactType.PhoneNumber) {
                const phone = parsePhoneNumber(text, "US");
                payload = phone ? phone.number : "";
            } else {
                payload = text;
            }

            res = await createContact(contactType, payload);
        } catch (e) {
            addToast("Failed to create contact");
            return;
        }

        await mutate();
        if (!res.verified) {
            setShowModal(true);
            setVerifyContact({ id: res.id, contact: res.value });
        }
        setShowAdd(true);
    };

    return (
        <EditInput
            value={text}
            onChange={onChange}
            onConfirm={onConfirm}
            onCancel={onCancel}
        />
    );
};

const MoreIndicator = ({
    onDelete,
    onMakePrimary,
    onReverify,
    isVerified,
    isPrimary,
}) => {
    const [isVisible, setIsVisible] = useState(false);
    const ref = useOnClickOutside(() => setIsVisible(false), !isVisible);
    return (
        <>
            <Span position="relative">
                <Indicator src="/more.svg" onClick={() => setIsVisible(true)} />
                <Dropdown ref={ref as any} isVisible={isVisible}>
                    {!isPrimary && isVerified && (
                        <DropdownItem
                            onClick={() => {
                                onMakePrimary();
                                setIsVisible(false);
                            }}
                        >
                            <Text weight="400" size="0.7rem">
                                Set primary
                            </Text>
                        </DropdownItem>
                    )}
                    <DropdownItem
                        onClick={() => {
                            onDelete();
                            setIsVisible(false);
                        }}
                    >
                        <Text weight="400" size="0.7rem">
                            Remove
                        </Text>
                    </DropdownItem>
                    {!isVerified && (
                        <DropdownItem
                            onClick={() => {
                                onReverify();
                                setIsVisible(false);
                            }}
                        >
                            <Text weight="400" size="0.7rem">
                                Verify
                            </Text>
                        </DropdownItem>
                    )}
                </Dropdown>
            </Span>
        </>
    );
};

export const ExistingInput = ({
    contactType,
    text,
    onDelete,
    onMakePrimary,
    onReverify,
    isPrimary,
    isVerified,
}) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);

    return (
        <Flex childMargin="0.2rem">
            {isVerified && <Indicator src="/greentick.png" />}
            <span>{text}</span>
            {isPrimary && (
                <Tag variant="primary">
                    <span>PRIMARY</span>
                </Tag>
            )}
            {!isVerified && (
                <Tag>
                    <span>UNVERIFIED</span>
                </Tag>
            )}
            {!isVerified || onDelete ? (
                <MoreIndicator
                    isPrimary={isPrimary}
                    isVerified={isVerified}
                    onDelete={() => setModalIsOpen(true)}
                    onMakePrimary={onMakePrimary}
                    onReverify={onReverify}
                />
            ) : undefined}
            <DeleteModal
                type={contactType}
                contact={text}
                show={modalIsOpen}
                onDelete={() => {
                    onDelete();
                    setModalIsOpen(false);
                }}
                closeFunc={() => setModalIsOpen(false)}
            />
        </Flex>
    );
};

export const AddInput = ({ text, onClick, margin }) => (
    <AddButton onClick={onClick} marginTop={margin}>
        {text}
    </AddButton>
);

export const EditInput = ({ onConfirm, value, onChange, onCancel }) => (
    <Flex childMargin="0.2rem" width="100%">
        <FormInput height="2rem" value={value} onChange={onChange} />
        <Button type="button" onClick={onConfirm}>
            Confirm
        </Button>
        <Indicator src="/x-circle.svg" width="1.3rem" onClick={onCancel} />
    </Flex>
);

const ContactInput = ({ route, addText, initialData, contactType }) => {
    const { addToast } = useToasts();
    const { data, mutate } = useResourceList<ContactInfo>(
        route,
        (id) => `${route}${id}/`,
        { initialData }
    );
    const [showAdd, setShowAdd] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [verifyContact, setVerifyContact] = useState({ id: 0, contact: "" });

    // Initial data provided
    const infolist = data!;

    return (
        <>
            {infolist.map(({ id, value, primary, verified }) => (
                <ExistingInput
                    contactType={contactType}
                    text={value}
                    onReverify={async () => {
                        try {
                            setVerifyContact({ id, contact: value });
                            await reverifyContact(contactType, id);
                        } catch (e) {
                            addToast(`Did not resend verification message - check your
${contactType === ContactType.Email ? "email" : "phone messages"} again.`);
                        }
                        setShowModal(true);
                    }}
                    onDelete={
                        contactType === "email" && infolist.length === 1
                            ? undefined
                            : async () => {
                                  try {
                                      await deleteContact(contactType, id);
                                  } catch (e) {
                                      addToast("Delete contact failed");
                                  }
                                  mutate();
                              }
                    }
                    onMakePrimary={() => mutate(id, { primary: true })}
                    key={id}
                    isPrimary={primary}
                    isVerified={verified}
                />
            ))}
            {showAdd && (
                <AddInput
                    text={addText}
                    margin={infolist.length === 0 && "0.6rem"}
                    onClick={() => {
                        setShowAdd(false);
                    }}
                />
            )}
            {!showAdd && (
                <FieldInput
                    mutate={mutate}
                    contactType={contactType}
                    setShowAdd={setShowAdd}
                    setShowModal={setShowModal}
                    setVerifyContact={setVerifyContact}
                    onCancel={() => setShowAdd(true)}
                />
            )}
            <VerificationModal
                type={contactType}
                show={showModal}
                id={verifyContact.id}
                contact={verifyContact.contact}
                closeFunc={() => setShowModal(false)}
                mutate={mutate}
            />
        </>
    );
};

export default ContactInput;
