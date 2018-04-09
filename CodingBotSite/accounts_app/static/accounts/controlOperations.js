//INPUT VALIDATION ISN'T IMPLEMENTED CURRENTLY
//COMMENTS CANNOT BE PROPERLY ADDED TO TEMPLATE LITERALS (` `) SO ALL COMMENTS WILL BE ABOVE THE FUNCTIONS
//ALL FORM SUBMISSION ARE SENT TO SELF AND NOT USED AT ALL

//Gives functionality to the popovers on Input fields
$(function(){
    $('[data-toggle="popover"]').popover()
  });
  
  //Function to display the Class Creation code in professor.html
  //All form-group rows are meant to align labels and input fields
  //HARDCODED: Pack Selection
  function createClass() {
      document.getElementById("professorView").innerHTML = 
      `
              <h1>Create a New Class</h1>
              <form action="professor.html" method="post" target="_self">
              <div class="form-group row">
                  <span class="col-sm-6">Class Name</span>
                  <span class="col-sm-6">Class Section</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="className">
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="classSection">
                  </div>
              </div>
              <div class="form-group row">
                  <span class="labels col-sm-6">Max Capacity</span>
                  <span class="labels col-sm-6">Class Code</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="number" name="maxCapacity" min="1">
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="classCode">
                  </div>
              </div>
              <div class="form-group row">
                  <span class="col-sm-6">Open Date for Enrollment</span>
                  <span class="col-sm-6">Close Date for Enrollment</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="date" name="openDate">
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="date" name="closeDate">
                  </div>
              </div>
              <span class="labels">Pack Selection</span>
              <div class="packOptions">
                  <input type="checkbox" name="packs" value="if"> If Pack<br />
                  <input type="checkbox" name="packs" value="string"> String Pack<br />
                  <input type="checkbox" name="packs" value="database"> Database Management Pack<br />
                  <input type="checkbox" name="packs" value="methods"> Methods Pack<br />
              </div>
              <button type="submit" class="btn btn-success">Submit</button>
              </form>
      `;
  }
  
  //Function to display the class view code for professor.html
  //Table responsive keeps table within div
  //Table hover creates grey highlight when mouse over table row
  //HARDCODED: Table Data
  function viewClass() {
      document.getElementById("professorView").innerHTML = 
      `
              <h1>Class 1</h1>
              <div class="table-responsive">
              <table class="table table-hover">
                  <thead>
                      <tr>
                          <th>Name</th>
                          <th>Email</th>
                          <th>Progress</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr>
                          <td>Michael Riggle</td>
                          <td>Micahel.Riggle@gmail.com</td>
                          <td>3/4 Packs Complete</td>
                      </tr>
                      <tr>
                          <td>Tanner Crowe</td>
                          <td>Tanner.Crowe@gmail.com</td>
                          <td>0/4 Packs Complete</td>
                      </tr>
                      <tr>
                          <td>Will Clayton</td>
                          <td>Will.Clayton@gmail.com</td>
                          <td>1/4 Packs Complete</td>
                      </tr>
                  </tbody>
              </table>
              </div>
              <button class="btn btn-success" type="button" onClick="editClass()">Edit Class</button>
      `;
  }
  
  //Function to display the edit class code for professor.html
  //disabled indicates the fields cannot be altered by the userAgent
  //HARDCODED: Values of all fields need to be filled by database including Pack Selection, Packs themselves are also hard coded
  function editClass() {
      document.getElementById("professorView").innerHTML =
      `
              <h1>Edit Class 1</h1>
              <form action="professor.html" method="post" target="_self">
              <div class="form-group row">
                  <span class="col-sm-6">Class Name</span>
                  <span class="col-sm-6">Class Section</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="className" value="Existing Class Name" disabled>
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="classSection" value="Existing Section" disabled>
                  </div>
              </div>
              <div class="form-group row">
                  <span class="col-sm-6">Max Capacity</span>
                  <span class="col-sm-6">Class Code</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="number" name="maxCapacity" min="1">
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="text" name="classCode">
                  </div>
              </div>
              <div class="form-group row">
                  <span class="col-sm-6">Open Date for Enrollment</span>
                  <span class="col-sm-6">Close Date for Enrollment</span>
              </div>
              <div class="form-group row">
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="date" name="openDate">
                  </div>
                  <div class="col-sm-6">
                  <input class="form-control-sm" type="date" name="closeDate">
                  </div>
              </div>
              <span>Pack Selection</span>
              <div class="packOptions">
                  <input type="checkbox" name="packs" value="if" checked> If Pack<br />
                  <input type="checkbox" name="packs" value="string"> String Pack<br />
                  <input type="checkbox" name="packs" value="database" checked> Database Management Pack<br />
                  <input type="checkbox" name="packs" value="methods"> Methods Pack<br />
              </div>
              <button type="submit" class="btn btn-success">Submit</button>
              </form>	
      `;
  }
  
  //Function to display the professor creation code for school.html
  //Basic form like the others with input fields for a professor account
  //HARDCODED: None
  function createProfessor() {
      document.getElementById("schoolView").innerHTML =
      `
      <h1>Create Professor Account</h1>
      <form action="school.html" method="post" target="_self">
      <div class="form-group row">
          <span class="col-sm-6">First Name</span>
          <span class="col-sm-6">Last Name</span>
      </div>
      <div class="form-group row">
          <div class="col-sm-6">
          <input class="form-control-sm" type="text" name="firstName">
          </div>
          <div class="col-sm-6">
          <input class="form-control-sm" type="text" name="lastName">
          </div>
      </div>
      <div class="form-group row">
          <span class="labels col-sm-6">Professor Email</span>
          <span class="labels col-sm-6">Password</span>
      </div>
      <div class="form-group row">
          <div class="col-sm-6">
          <input class="form-control-sm" type="email" name="professorEmail">
          </div>
          <div class="col-sm-6">
          <input class="form-control-sm" type="password" name="professorPassword">
          </div>
      </div>
      <button type="submit" class="btn btn-success">Submit</button>
      </form>
      `;
  }
  
  //Function to display the account management code for school.html
  //Another table with extra headers for edit and delete functionality
  //HARDCODED: Table Data, Filter Options do nothing, Edit & Delete do nothing
  function viewAccounts() {
      document.getElementById("schoolView").innerHTML = 
      `
      <h1>Account Management</h1>
      <select>
          <option value="all">All Accounts</option>
          <option value="professors">Professor Accounts</option>
          <option value="students">Student Accounts</option>
      </select>
      <div class="table-responsive">
      <table class="table table-hover">
          <thead>
              <tr>
                  <th>Type</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th></th>
                  <th></th>
              </tr>
          </thead>
              <tbody>
              <tr>
                  <td>Professor</td>
                  <td>Michael Riggle</td>
                  <td>Micahel.Riggle@gmail.com</td>
                  <td><button class="btn btn-info" type="button">Edit</button></td>
                  <td><button class="btn btn-danger" type="button">Delete</button></td>
              </tr>
              <tr>
                  <td>Student</td>
                  <td>Tanner Crowe</td>
                  <td>Tanner.Crowe@gmail.com</td>
                  <td><button class="btn btn-info" type="button">Edit</button></td>
                  <td><button class="btn btn-danger" type="button">Delete</button></td>
              </tr>
              <tr>
                  <td>Student</td>
                  <td>Will Clayton</td>
                  <td>Will.Clayton@gmail.com</td>
                  <td><button class="btn btn-info" type="button">Edit</button></td>
                  <td><button class="btn btn-danger" type="button">Delete</button></td>
              </tr>
          </tbody>
      </table>
      </div>		
      `
  }