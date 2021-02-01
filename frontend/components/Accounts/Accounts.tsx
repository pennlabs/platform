import React from "react";
import { Field, Form, Formik } from "formik";
import { User } from "../../types";
import { doApiRequest } from "../../utils/fetch";
import generateLoadOption from "../../data-fetching/accounts";
import SelectField from "./SelectField";
import { useResource } from "@pennlabs/rest-hooks";


const Accounts = ({ user }: { user: User }) => {
    // TODO: use swr?
    // const {data: finalUser} = useResource("/accounts/me/", {
    //     initialData: user
    // });
    // console.log(finalUser)
    return (
    <Formik
        initialValues={user}
        onSubmit={(values, actions) => {
            doApiRequest("/accounts/me/", {
                method: "PATCH",
                body: values,
            }).catch((err) => console.log(err));
            // TODO: better error checking (toast?)
            console.log({ values, actions });
            actions.setSubmitting(false);
        }}
    >
        <Form>
            PennKey: {user.username}
            <br />
            <label htmlFor="first_name">Preferred First Name</label>
            <Field name="first_name" className="form-input" />
            <br />
            Last Name: {user.last_name}
            <br />
            {user.groups.includes("student") && (
                <div>
                    <b>Student:</b>
                    <br />
                    <label htmlFor="student.graduation_year">
                        Graduation Year
                    </label>
                    <Field
                        name="student.graduation_year"
                        className="form-input"
                    />
                    <Field
                        name="student.major"
                        component={SelectField}
                        loadOptions={generateLoadOption("majors")}
                    />
                    <Field
                        name="student.school"
                        component={SelectField}
                        loadOptions={generateLoadOption("schools")}
                    />
                </div>
            )}
            <b>Phone Numbers:</b>
            <br/>
            + Add another phone number
            <br/>
            <b>Emails:</b>
            <br/>
            + Add another email
            <br/>
            <button type="submit">Submit</button>
        </Form>
    </Formik>
)};

export default Accounts;
