import VerificationInput from "react-verification-input";
import { Modal } from "react-bulma-components";

import { mutateResourceListFunction } from "@pennlabs/rest-hooks/dist/types";
import toast from "react-hot-toast";
import styles from "../../../styles/Verification.module.css";
import { verifyContact } from "../../../data-fetching/accounts";
import { ContactType, ContactInfo } from "../../../types";
import { logException } from "../../../utils/sentry";
import { Flex } from "../ui";

interface VerificationFormProps {
    type: ContactType;
    id: number;
    closeFunc: () => void;
    mutate: mutateResourceListFunction<ContactInfo>;
}

const VerificationForm = (props: VerificationFormProps) => {
    const { type, id, closeFunc, mutate } = props;
    const handleInputChange = async (value: string) => {
        if (value.length === 6) {
            try {
                await verifyContact(type, id, value);
                closeFunc();
                mutate();
                toast.success("Verification success!");
            } catch (e: any) {
                // TODO: read up on error handling
                toast.error("Verification failed");
                logException(e);
            }
        }
    };
    return (
        <VerificationInput
            length={6}
            onChange={handleInputChange}
            validChars="0-9"
            classNames={{
                container: styles.container,
                character: styles.character,
                characterSelected: styles["character--selected"],
            }}
            removeDefaultStyles
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
                <Modal.Card.Header onClose={closeFunc}>
                    <Modal.Card.Title>
                        Verify your {prettyType}
                    </Modal.Card.Title>
                </Modal.Card.Header>
                <Modal.Card.Body>
                    Please enter the 6 digit confirmation code sent to {contact}
                    :
                    <Flex>
                        <VerificationForm
                            type={type}
                            id={id}
                            closeFunc={closeFunc}
                            mutate={mutate}
                        />
                    </Flex>
                </Modal.Card.Body>
            </Modal.Card>
        </Modal>
    );
};

export default VerificationModal;
