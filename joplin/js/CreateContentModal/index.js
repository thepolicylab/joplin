import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

import ChooseTypeStep from './ChooseTypeStep.js';
import ChooseTitleStep from './ChooseTitleStep.js';
import ChooseTopicStep from './ChooseTopicStep.js';
import ButtonBar from './ButtonBar.js';

import './index.scss';

const MAX_TITLE_LENGTH = 58;
const THEME_TOPIC_TREE = window.themeTopicsTree;

class CreateContentModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      activeStep: 0,
      titleCharacterCount: 0,
    };
  }

  onLastStep = () => {
    return (
      // Skip Topic Select Step for creating a Department
      (this.state.type === 'department' && this.state.activeStep === 1) ||
      this.state.activeStep === 2
    );
  };

  incrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep + 1,
    });
  };

  decrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep - 1,
    });
  };

  handleNextButton = e => {
    // Validate title max length
    if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

    // Validate title min length
    if (this.state.titleCharacterCount <= 0) return false;

    // If we're on the topic select step we need a topic selected
    if (this.state.activeStep === 2 && this.state.topic === null) return false;

    if (this.onLastStep()) {
      this.createPage();
      return;
    }

    this.incrementActiveStep();
  };

  handleBackButton = e => {
    this.decrementActiveStep();
  };

  handleTypeSelect = (dataObj, e) => {
    this.setState({
      type: dataObj.type,
    });
    this.incrementActiveStep();
  };

  handleTitleInputChange = e => {
    this.setState({
      title: e.target.value,
      titleCharacterCount: e.target.value.length,
    });
  };

  handleTopicSelect = id => {
    this.setState({ topic: id });
  };

  redirectToEditPage = id => {
    window.location.href = `/admin/pages/${id}/edit/`;
  };

  createPage = () => {
    axios
      .post(
        '/admin/pages/new_from_modal/',
        {
          type: this.state.type,
          title: this.state.title,
          topic: this.state.topic,
        },
        { headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      )
      .then(response => {
        this.redirectToEditPage(response.data.id);
      })
      .catch(error => {
        console.log(error);
      })
      .bind(this);
  };

  handleCloseButton = e => {
    this.setState({
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      activeStep: 0,
      redirectUrl: null,
      titleCharacterCount: 0,
    });
  };

  render() {
    return (
      <div
        className="modal fade"
        id="createNewContentModal"
        tabIndex="-1"
        role="dialog"
        aria-labelledby="createNewContentModalLabel"
      >
        <div className="CreateContentModal__wrapper">
          <div className="modal-dialog" role="document">
            <div className="modal-content CreateContentModal">
              <div className="modal-body">
                {this.state.activeStep === 0 && (
                  <ChooseTypeStep handleTypeSelect={this.handleTypeSelect} />
                )}
                {this.state.activeStep === 1 && (
                  <ChooseTitleStep
                    pageType={this.state.type}
                    title={this.state.title}
                    handleTitleInputChange={this.handleTitleInputChange}
                    characterCount={this.state.titleCharacterCount}
                    maxCharacterCount={MAX_TITLE_LENGTH}
                  />
                )}
                {this.state.activeStep === 2 && (
                  <ChooseTopicStep
                    topic={this.state.topic}
                    handleTopicSelect={this.handleTopicSelect}
                    themeTopicTree={THEME_TOPIC_TREE}
                  />
                )}
                <ButtonBar
                  handleBackButton={this.handleBackButton}
                  handleNextButton={this.handleNextButton}
                  handleCloseButton={this.handleCloseButton}
                  hidden={this.state.activeStep === 0}
                  onLastStep={this.onLastStep()}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <CreateContentModal />,
  document.getElementById('coa-CreateContentModal'),
);