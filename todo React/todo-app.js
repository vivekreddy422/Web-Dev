function Task(props) {
    return( 
        (<div style={{display:'flex', justifyContent:'left'}}>
            <li style = {{textDecoration: props.t.complete ? 'line-through' : ""}}>
                {props.t.name},
                {props.dueDate.toLocaleTimeString()},
            </li>
            <input 
                type="checkbox" 
                value="checkbox" 
                onClick = {props.toggleComplete}
            />
            <input type="submit" value="Delete" onClick =  {() => {props.onDelete(props.id)} }  />
        </div>)
    );
}

class TodoList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {list: props.list, isStrikeThrough: false};

        // this.handleAddTask = this.handleAddTask.bind(this);
        // this.handleDeleteTask = this.handleDeleteTask.bind(this);
    }

    handleDeleteTask = (id) => {
        console.log(this)
        console.log("delete task clicked with ID :", id);
        let list = this.state.list
        list = list.filter(task => task.id != id)
        this.setState({list : list})
    }

    handleAddTask = (task) => {
        console.log("add task clicked");
        this.state.list.push(task);
        this.setState({list: this.state.list})
    }

    toggleComplete = (id) => {
        this.setState({
            list : this.state.list.map(task => {
                if (task.id === id) {
                    return {
                        ...task,
                        complete : !task.complete
                    }
                } else {
                    return task
                }
            })
        })
    }

    render() {
        return (
            <div>
                <h1>TODO List</h1>
                <ol>
                    {
                    this.state.list.map((t) =>
                        <Task key={t.id} id={t.id} t={t} dueDate={t.dueDate} toggleComplete={() => this.toggleComplete(t.id)}
                        onDelete={this.handleDeleteTask}/>)
                    }
                </ol>
                <TaskNameForm onAddTask={this.handleAddTask} />
            </div>
        );
    }
}

class TaskNameForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        const taskList = this.props.taskList;
        // create a task object
        event.preventDefault();
        const task = {id:Date.now(), name: this.state.value, dueDate: new Date(), complete:false};
        // add the task object to the task list
        this.props.onAddTask(task);
        this.setState({value:""})
    }

    handleChange(event) {
        // code to set the state of the component
        this.setState({value: event.target.value});
    }

    render() {
        return(
            <form onSubmit={this.handleSubmit}>
                <input type="text" placeholder="todo...." onChange={this.handleChange} required/>
                <input type="submit" value="Add Task" />
            </form>
        );
    }
}

ReactDOM.render(
    <TodoList list={[]} />,
    document.getElementById('todo')
);