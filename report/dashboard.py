from fasthtml.common import *
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE
from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team

# import the load_model function from the utils.py file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report.utils import load_model
"""
Below, we import the parent classes
you will use for subclassing
"""
from report.base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from report.combined_components import FormGroup, CombinedComponent
from report.base_components.matplotlib_viz import LineChart, BarChart

# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def __init__(self, id="selector", name="user-selection", label=""):
        # Apelăm constructorul părinte cu aceiași parametri
        super().__init__(id=id, name=name, label=label)

    def build_component(self, entity_id, model):
        #options = model.get_names()
        #self.options = [(id_, name) for id_, name in options]
        #self.value = entity_id
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = model.name
        options = model.get_user_type_names_and_ids()
        if entity_id is None and options:
            entity_id = options[0][0]
        self.value = entity_id
        select = super().build_component(entity_id, model)
        select.attrs["hx-include"] = "closest form [name='profile_type']"

        # Return the output from the
        # parent class's build_component method
        return select
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
    def component_data(self, entity_id, model):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        result = model.get_user_type_names_and_ids()
        # Dacă evenimentele sunt un DataFrame (folosit în multe metode)
        print(f"DEBUG: component_data returns: {result}")
        # Dacă evenimentele sunt o listă de tuple
        #return result
        return [(id, name) for id, name in result]
        # Create a subclass of base_components/BaseComponent
        # called `Header`
        #### YOUR CODE HERE
class Header(BaseComponent):
    def __init__(self):
        super().__init__()
    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE
    def build_component(self, entity_id, model):
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        #### YOUR CODE HERE
        return H1(model.name)
# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
    def __init__(self, title="Line Chart"):
        self.title = title
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model):
        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        #### YOUR CODE HERE
        df = model.model_data(entity_id)
        print(f"DEBUG: DataFrame shape: {df.shape} columns: {df.columns.tolist()}")
        if df.empty:
            print("DEBUG: DataFrame is empty!")
            return H4("Datele nu sunt disponibile.")
        if not all(col in df.columns for col in ["event_date", "positive_events", "negative_events"]):
            print("DEBUG: Lipsesc coloanele așteptate în DataFrame.")
            return H4("Datele nu sunt disponibile sau lipsesc coloanele așteptate.")
        # Use the pandas .fillna method to fill nulls with 0
        #### YOUR CODE HERE
        df = df.fillna(0)
        df = df.groupby("event_date")[["positive_events", "negative_events"]].sum()
        #x = df["event_type"]
        #y = df["event_count"]
        # User the pandas .set_index method to set
        # the date column as the index
        #### YOUR CODE HERE
        #df = df.set_index("event_type")
        # Sort the index
        #### YOUR CODE HERE
        df = df.sort_index().cumsum()
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        #df = df.cumsum()
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ['Positive', 'Negative']
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        print(f"DEBUG: DataFrame după preprocesare:\n{df.head()}")
        fig, ax = plt.subplots()
        # call the .plot method for the
        # cumulative counts dataframe
        df.plot(ax=ax)
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set
        # the border color and font color to black.
        # Reference the base_components/matplotlib_viz file
        # to inspect the supported keyword arguments
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
	    # Set title and labels for x and y axis
        # Set title and labels
       	ax.set_title(self.title)
        ax.set_xlabel("Event Type")
        ax.set_ylabel("Cumulative Event Count")
        return fig
# Create a subclass of base_components/MatplotlibViz
# called `BarChart`

class BarChart(MatplotlibViz):
    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()
    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model):
        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE
        data = model.model_data(entity_id)
        # Verifică dacă predictorul are atributul feature_names_in_
        # și filtrează coloanele DataFrame-ului pentru a păstra doar ce trebuie
        if hasattr(self.predictor, 'feature_names_in_'):
            expected_features = self.predictor.feature_names_in_
            # Selectează doar coloanele pe care modelul le așteaptă
            data = data[expected_features]
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE
        proba = self.predictor.predict_proba(data)
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE
        proba_scores = proba[:, 1]
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE
        if getattr(model, 'name', None) == "team":
            pred = proba_scores.mean()
        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE
        else:
            # Otherwise, set pred to the first value of the predict_proba output
            pred = proba_scores[0]
            # Initialize a matplotlib subplot
            #### YOUR CODE HERE
        fig, ax = plt.subplots()
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        # Create a subclass of combined_components/CombinedComponent
        # called Visualizations
        #### YOUR CODE HERE
        return fig
class Visualizations(CombinedComponent):
    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE
    children = [LineChart(title="Events Over Time"), BarChart()]
    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
    # Create a subclass of base_components/DataTable
    # called `NotesTable`
    #### YOUR CODE HERE
class NotesTable(DataTable):
    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE
    def component_data(self, entity_id, model):
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes
        # method. Return the output
        #### YOUR CODE HERE
        return model.notes()
class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method="POST"
    hx_post    = "/update_data"
    hx_trigger = "change"
    hx_swap    = "none"
    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            #hx_get='/update_dropdown',
            #hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]
# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE
class Report(CombinedComponent):
    def __init__(self):
        self.children = [
            Header(),
            DashboardFilters(),
            Visualizations(),
            NotesTable()
        ]
        super().__init__(components=self.children)

    def __call__(self, entity_id, model):
        print(f"DEBUG: Rendering Report for entity_id={entity_id}, model={model}")
        return super().__call__(entity_id, model)

    def __str__(self):
        return f"""
        <html>
        <head>
            <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        </head>
        <body>
            {super().__str__()}
        </body>
        </html>
        """

# Run the app if this script is executed directly
#if __name__ == "__main__":
#    app.run()
# Initialize the `Report` class

report = Report()
# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE
    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result

app = FastHTML(
    title="Recruitment Report",
    description="A dashboard for viewing recruitment data",
    component=report,  # folosești exact aceeași instanță aici
    scripts=["https://unpkg.com/htmx.org@1.9.2"]
)

@app.route("/", methods=["GET"])
def root_route():
    entity_id = 1
    model = Employee(entity_id)  # create an instance of Employee
    output = report(entity_id, model)  # Salvează rezultatul
    print(f"DEBUG: Report output type: {type(output)}")  # Afișează tipul corect
    return str(output)
# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`.
# parameterize the employee ID
# to a string datatype
#### YOUR CODE HERE
    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    model = Employee(employee_id)
    if model.name == "Unknown":
        raise HTTPException(status_code=404, detail="Employee not found")
    return str(report(employee_id, model))

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`.
# parameterize the team ID
# to a string datatype
#### YOUR CODE HERE
    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
@app.get("/team/{team_id}")
def get_team(team_id: int):
    model = Team(team_id)
    if model.name == "Unknown":
        raise HTTPException(status_code=404, detail="Team not found")
    return str(report(team_id, model))

@app.route("/.well-known/appspecific/com.chrome.devtools.json", methods=["GET"])
def chrome_well_known():
    return Response(status_code=204)

# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

serve()
