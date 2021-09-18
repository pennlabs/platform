import { mutateResourceFunction } from "@pennlabs/rest-hooks/dist/types";
import React from "react";
import { Modal, Button } from "react-bulma-components";
import { deleteContact } from "../../data-fetching/accounts";
import { ContactType, User } from "../../types";
import { logException } from "../../utils/sentry";

interface DeleteModalProps {
    type: ContactType;
    id: number;
    contact: string;
    show: boolean;
    closeFunc: () => void;
    mutate: mutateResourceFunction<User>;
}

const DeleteModal = (props: DeleteModalProps) => {
    const { show, closeFunc, type, contact, id, mutate } = props;
    const prettyType = type === ContactType.Email ? "email" : "phone number";
    const deleteContactMethod = async () => {
        try {
            await deleteContact(type, id);
            closeFunc();
            mutate();
            // TODO: toast
        } catch (e) {
            logException(e);
            // TODO: toast
        }
    };
    return (
        <Modal show={show} onClose={closeFunc}>
            <Modal.Card>
                <Modal.Card.Header onClose={closeFunc}>
                    <Modal.Card.Title>{`Remove ${prettyType}?`}</Modal.Card.Title>
                </Modal.Card.Header>
                <Modal.Card.Body>
                    {`You will no longer be able to use ${contact} with your account.`}
                    <Button>Cancel</Button>
                    <Button>Remove</Button>
                </Modal.Card.Body>
            </Modal.Card>
        </Modal>
    );
};

export default DeleteModal;
