---
name: New generic component
about: Request for new library component(s)
title: "[Alias, see table below] - [short description]"
labels: libraries-request - GENERIC
assignees: ''

---

| Description            | Field                                          |
|:-----------------------|:-----------------------------------------------|
| Project                | [Intended project for the component]            |
| Alias (file name)      | [Norm + measure] OR [manufacturer + code] [^1] |
| Applicant              | Name Surname, @username                        |
| Supervisor             | Name Surname, @username                        |
| Maintainer             | Lorenzo Protopapa, @Lawproto                   |
| Coworkers              | @icub-tech-iit/silo-mech                       |

### Notes:

### Checklist:
Complete the checklist in order to fulfill the request.

- [ ] Create a new part file using the [start part commercial](https://github.com/icub-tech-iit/cad-libraries/wiki/Mechanical-design-guidelines#standard-part-for-commercial-components) Creo template.
- [ ] Check if one [special case](https://github.com/icub-tech-iit/cad-libraries/wiki/Mechanical-design-guidelines#special-cases-and-examples) applies to this component.
- [ ] If an external file like STEP, IGS, etc. needs to be imported to create the geometry of the part,  link that file in a new comment.
- [ ] Create an IIT code in [WinGST](http://wingst.icub.iit.local/) with at least one manufacturer and related supplier.
- [ ] If a datasheet with useful information is available, create a copy in a shared path and link it inside the IIT code in WinGST.
- [ ] Assign [mass properties](https://github.com/icub-tech-iit/cad-libraries/wiki/Mechanical-design-guidelines#mass-properties-of-commercial-parts) to the part after measuring real life weight.[^2]
- [ ] Convert the file with the [EDU to COM license](https://github.com/icub-tech-iit/cad-libraries/wiki/PTC-Creo-Guidelines#save-file-with-commercial-license).

[^1]: For more details, see our [standard convention](https://github.com/icub-tech-iit/cad-libraries/wiki/Mechanical-design-guidelines#commercial-components-coding-standard) for Aliases.
[^2]: For simple, uniform objects like bars, screws, bushings, etc. the proper material can be assigned instead.
