import React, { useRef } from "react";
import ReactCodeInput from "react-code-input";
import { useToasts } from "react-toast-notifications";
import { Modal } from "react-bulma-components";
import { mutateResourceListFunction } from "@pennlabs/rest-hooks/dist/types";
import { verifyContact } from "../../../data-fetching/accounts";
import { ContactType, ContactInfo } from "../../../types";
import { logException } from "../../../utils/sentry";

// TODO: combine some of these types
interface VerificationFormProps {
    type: ContactType;
    id: number;
    closeFunc: () => void;
    mutate: mutateResourceListFunction<ContactInfo>;
    // toastFunc: (Toast) => void;
}

interface CodeInputRefState {
    input: string[];
}

interface CodeInputRef extends ReactCodeInput {
    textInput: HTMLInputElement[];
    value: string;
    state: CodeInputRefState;
}

const VerificationForm = (props: VerificationFormProps) => {
    const { addToast } = useToasts();
    const { type, id, closeFunc, mutate } = props;
    const codeInput = useRef<CodeInputRef>(null);
    const handleInputChange = async (value: string) => {
        if (value.length === 6) {
            try {
                await verifyContact(type, id, value);
                closeFunc();
                mutate();
                addToast("Verification success!");
            } catch (e) {
                addToast("Verification failed");
                logException(e);
            }
        }
    };
    return (
        <ReactCodeInput
            name="verification"
            fields={6}
            onChange={handleInputChange}
            ref={codeInput}
            inputMode="numeric"
        />
    );
};

interface VerificationModalProps {
    type: ContactType;
    id: number;
    contact: string;
    show: boolean;
    closeFunc: () => void;
    mutate: mutateResourceListFunction<ContactInfo>;
}
const VerificationModal = (props: VerificationModalProps) => {
    const { show, closeFunc, type, contact, id, mutate } = props;
    const prettyType = type === ContactType.Email ? "Email" : "Phone Number";
    return (
        <Modal show={show} onClose={closeFunc}>
            <Modal.Card>
                <Modal.Card.Head onClose={closeFunc}>
                    <Modal.Card.Title>
                        Verify your {prettyType}
                    </Modal.Card.Title>
                </Modal.Card.Head>
                <Modal.Card.Body>
                    Please enter the 6 digit confirmation code sent to {contact}
                    :
                    <VerificationForm
                        type={type}
                        id={id}
                        closeFunc={closeFunc}
                        mutate={mutate}
                    />
                </Modal.Card.Body>
            </Modal.Card>
        </Modal>
    );
};

export default VerificationModal;
