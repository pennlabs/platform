import {
    ChangeEventHandler,
    FormEvent,
    Dispatch,
    useState,
    MutableRefObject,
    useEffect,
    useRef,
} from "react";
import styled from "styled-components";
import { useResourceList } from "@pennlabs/rest-hooks";
import parsePhoneNumber from "libphonenumber-js";
import { mutateResourceListFunction } from "@pennlabs/rest-hooks/dist/types";

import toast from "react-hot-toast";
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
import VerificationModal from "../modals/verification";
import DeleteModal from "../modals/delete";
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

type VerifyContactState = {
    id: number;
    contact: string;
};

interface FieldInputProps {
    mutate: mutateResourceListFunction<ContactInfo>;
    contactType: ContactType;
    setShowAdd: Dispatch<boolean>;
    setVerifyContact: Dispatch<VerifyContactState>;
    setShowModal: Dispatch<boolean>;
    onCancel: () => void;
}

const FieldInput = ({
    mutate,
    contactType,
    setShowAdd,
    setVerifyContact,
    setShowModal,
    onCancel,
}: FieldInputProps) => {
    const [text, setText] = useState("");

    const onChange = (e: FormEvent<HTMLInputElement>) => {
        setText(e.currentTarget.value);
    };

    const onConfirm = async () => {
        if (!text.trim().length) {
            toast.error("Please enter a value!");
            return;
        }
        let res;

        try {
            let payload;

            if (contactType === ContactType.PhoneNumber) {
                const phone = parsePhoneNumber(text, "US");
                if (!phone) {
                    toast.error("Invalid phone number");
                    return;
                }
                payload = phone ? phone.number.toString() : "";
            } else {
                payload = text;
            }

            res = await createContact(contactType, payload);
        } catch (e) {
            toast.error("Failed to create contact");
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

interface ContactEventProps {
    onDelete: () => void;
    onMakePrimary: () => void;
    onReverify: () => void;
    isVerified: boolean;
    isPrimary: boolean;
}

const MoreIndicator = ({
    onDelete,
    preventDeletion,
    onMakePrimary,
    onReverify,
    isVerified,
    isPrimary,
}: ContactEventProps & { preventDeletion: boolean }) => {
    const [isVisible, setIsVisible] = useState(false);
    const ref = useOnClickOutside(() => setIsVisible(false), !isVisible);
    return (
        <Span position="relative">
            <Indicator
                src="/more.svg"
                clickable
                onClick={() => setIsVisible(true)}
            />
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
                {preventDeletion || (
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
                )}
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
    preventDeletion,
}: ContactEventProps & {
    contactType: ContactType;
    text: string;
    preventDeletion: boolean;
}) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const showMoreIndicator = !preventDeletion || !isVerified;

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
            {showMoreIndicator ? (
                <MoreIndicator
                    isPrimary={isPrimary}
                    isVerified={isVerified}
                    onDelete={() => setModalIsOpen(true)}
                    preventDeletion={preventDeletion}
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

export const AddInput = ({
    text,
    onClick,
    margin,
}: {
    text: string;
    onClick: () => void;
    margin: string | undefined;
}) => (
    <AddButton onClick={onClick} marginTop={margin}>
        {text}
    </AddButton>
);

export const EditInput = ({
    onConfirm,
    value,
    onChange,
    onCancel,
}: {
    onConfirm: () => void;
    value: string;
    onChange: ChangeEventHandler<HTMLInputElement>;
    onCancel: () => void;
}) => {
    const inputRef = useRef<HTMLInputElement>(null);
    useEffect(() => {
        inputRef.current!.focus();
    }, []);
    return (
        <Flex childMargin="0.2rem" width="100%">
            <FormInput
                height="2rem"
                value={value}
                onChange={onChange}
                onKeyPress={(evt) => {
                    const event = evt || window.event;
                    if (event.key === "Enter") {
                        onConfirm();
                    }
                }}
                // TODO: maybe make this cancel when clicking outside...
                // onBlur={() => {
                //   setTimeout(onCancel, 100)
                // }}
                ref={inputRef}
            />
            <Button type="button" onClick={onConfirm}>
                Confirm
            </Button>
            <Indicator src="/x-circle.svg" width="1.3rem" onClick={onCancel} />
        </Flex>
    );
};

interface ContactInputProps {
    route: string;
    addText: string;
    initialData: ContactInfo[];
    contactType: ContactType;
}

const ContactInput = ({
    route,
    addText,
    initialData,
    contactType,
}: ContactInputProps) => {
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
                    preventDeletion={
                        infolist.length === 1 && contactType === "email"
                    }
                    onReverify={async () => {
                        try {
                            setVerifyContact({ id, contact: value });
                            await reverifyContact(contactType, id);
                        } catch (e) {
                            toast.error(
                                `Did not resend verification message - check your ${
                                    contactType === ContactType.Email
                                        ? "email"
                                        : "phone messages"
                                } again.`
                            );
                        }
                        setShowModal(true);
                    }}
                    onDelete={async () => {
                        try {
                            await deleteContact(contactType, id);
                        } catch (e) {
                            toast.error("Delete contact failed");
                        }
                        mutate();
                    }}
                    onMakePrimary={() => mutate(id, { primary: true })}
                    key={id}
                    isPrimary={primary}
                    isVerified={verified}
                />
            ))}
            {showAdd && (
                <AddInput
                    text={addText}
                    margin={infolist.length === 0 ? "0.6rem" : undefined}
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
