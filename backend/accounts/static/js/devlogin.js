const data = JSON.parse(document.getElementById('user_data').textContent);

const headers = [
    "Name",
    "Preferred Name",
    "Groups",
    "Email(s)",
    "Email Verified",
    "Phone #(s)",
    "Phone Verified",
    "Major(s)",
    "School(s)"
]

function parseRow(row) {
    let rowData = []
    // name
    rowData.push(row.first_name + " " + row.last_name)
    // preferred name
    rowData.push(rowData[0])
    // groups
    rowData.push(row.groups.join(", "))

    let {value: emails, verified: emailsVerified} = row.emails[0]
    for (let i = 1; i < row.emails.length; i++) {
        emails = emails + ", " + row.emails[i].value
        emailsVerified = emailsVerified + ", " + row.emails[i].verified
    }
    rowData.push(emails)
    rowData.push(emailsVerified)

    let {value: phones, verified: phonesVerified} = row.phone_numbers[0]
    for (let i = 1; i < row.phone_numbers.length; i++) {
        phones = phones + ", " + row.phone_numbers[i].value
        phonesVerified = phonesVerified + ", " + row.phone_numbers[i].verified
    }

    rowData.push(phones)
    rowData.push(phonesVerified)

    let majors = ""
    let schools = ""
    if (row.student.graduation_year) {
        const majorsData = row.student.major
        majors = majorsData[0].name + " " + majorsData[0].degree_type
        const schoolsData = row.student.school
        schools = schoolsData[0].name

        for (let i = 1; i < majorsData.length; i++) {
            majors = majors + ", " + majorsData[i].name + " " + majorsData[0].degree_type
        }

        for (let i = 1; i < schoolsData.length; i++) {
            schools = schools + ", " + schoolsData[i].name
        }

    }
    rowData.push(majors)
    rowData.push(schools)
    return rowData
}

function addTable() {
    let table = document.createElement("table")

let header = table.insertRow(-1)

for (let i = 0; i < headers.length; i++) {
    let th = document.createElement("th")
    th.innerHTML = headers[i]
    header.appendChild(th)
}

for (let i = 0; i < data.length; i++) {
    let rowData = parseRow(data[i])

    let tr = table.insertRow(-1)

    for (let j = 0; j < rowData.length; j++) {
        let cell = tr.insertCell(-1)
        cell.innerHTML = rowData[j]
    }
}

table.classList.add("table", "table-striped", "center-div")
let container = document.getElementById("datatable")
    container.appendChild(table)
}

addTable()
