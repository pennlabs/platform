import { mutateResourceFunction } from "@pennlabs/rest-hooks/dist/types";
import React from "react";
import { Modal } from "react-bulma-components";
import { ContactType, User } from "../../../types";
import VerificationForm from "./VerificationForm";

interface VerificationModalProps {
    type: ContactType;
    id: number;
    contact: string;
    show: boolean;
    closeFunc: () => void;
    mutate: mutateResourceFunction<User>;
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
