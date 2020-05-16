import React, { useState, Component } from 'react';
import { StyleSheet, Text, View, Button, TextInput } from 'react-native';
import Task from "./components/Task";
import DatePicker from 'react-native-datepicker';

export default class ToDoList extends Component {
  constructor(props) {
    super(props);
    this.state = {taskList: [], taskName:'', dueDate: ''}

    this.deleteTask = this.deleteTask.bind(this)
    this.markTask = this.markTask.bind(this)
  }

  //set taskName
  setTaskName(taskName) {
    this.setState({taskName: taskName})
  }

  //add task to the taskList
  addTask(taskName) {
    let task = {taskName: taskName, marked: false, dueDate: this.state.dueDate}
    this.state.taskList.push(task)
    this.setState({taskList: this.state.taskList, dueDate:"", taskName:""})
  }

  //mark the task in taskList
  markTask(taskName) {
    this.tempList = this.state.taskList.filter((task) => {
      if (task.taskName != taskName) {
        return task;
      } else {
        task.marked = !task.marked;
        return task;
      }
    })
    this.setState({taskList: this.tempList})

  }

  //delete task from taskList
  deleteTask(taskName) {
    this.tempList = this.state.taskList.filter((task) => {
      if (task.taskName != taskName) {
        return task
      }
    })
    this.setState({taskList: this.tempList})
  }
  render() {
    return ( 
      <View style={styles.container}>
        <Text>My TO-DO List</Text>
        <TextInput placeholder="Enter the taskName....." onChangeText={text => this.setTaskName(text)} value={this.state.taskName}/>
        <DatePicker date={this.state.dueDate} mode="date" placeholder="select date" format="YYYY-MM-DD" minDate={new Date()}
         onDateChange={(date) => {this.setState({dueDate: date})}} value={this.state.dueDate}/>

        <Button title="Add Task" onPress={() => this.addTask(this.state.taskName)}/>

        {
          this.state.taskList.map((task) => <Task task={task} deleteTask={this.deleteTask} markTask={this.markTask}/>)
        }
      </View>
    );
  }
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
