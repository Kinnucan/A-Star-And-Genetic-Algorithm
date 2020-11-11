"""  =================================================================
File: ALifeGUI.py

This file contains code, including a Tkinter class, that implements the
GUI for this problem.  This must be run in Python 3!
 ==================================================================="""

#
import time
from tkinter import *
import tkinter.filedialog as tkFileDialog

from aLifeSim import ALifeSim
from LocalSearchSolver import RulesetState, HillClimber   # TODO: Add GA searcher here


class ALifeGUI:
    """Set up and manage all the variables for the GUI interface."""
    
    def __init__(self, gridDim, numAgents=10, maxSteps=100):
        """Given the dimension of the grid, and the number of agents set up a new Tk object of the right size"""
        self.root = Tk()
        self.root.title("Susan Fox's Local Search ALife Simulation")
        self.gridDim = gridDim
        self.numberAgents = numAgents
        self.maxSteps = maxSteps
        self.currSteps = 0
        self.delayTime = 0.01
        self.sim = ALifeSim(self.gridDim, self.numberAgents)

        # Variables to hold the results of a simulation
        self.minTime = None
        self.maxTime = None
        self.avgTime = None
        self.agentsLiving = 0



    def setupWidgets(self):
        """Set up all the parts of the GUI."""
        # Create title frame and main buttons
        self._initTitle()

        # Create control buttons
        self._initGridBuildingTools()

        # Create the maze grid
        self._initGrid()

        # Create the search frame
        self._initSimTools()

        # Create the message frame
        self._initMessage()

        # Create the search alg frame
        self._initSearchTools()


              
    def goProgram(self):
        """This starts the whole GUI going"""
        self.root.mainloop()


    ### =================================================================
    ### Widget-creating helper functions
        
    def _initTitle(self):
        """Sets up the title section of the GUI, where the Quit and Help buttons are located"""
        titleButtonFrame = Frame(self.root, bd=5, padx=5, pady=5)
        titleButtonFrame.grid(row=1, column=1)
        quitButton = Button(titleButtonFrame, text="Quit", command=self.quit)
        quitButton.grid(row=1, column=1, padx=5)

        titleFrame =  Frame(self.root, bd=5, padx=5, pady=5)
        titleFrame.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        titleLabel = Label(titleFrame, text="Susan's Local Search ALife Simulation", font="Arial 20 bold",
                           anchor=CENTER, padx=5, pady=5)
        titleLabel.grid(row=1, column=1)

    

    def _initMessage(self):
        """Sets up the section of the window where messages appear, errors, failures, and numbers
        about how much work was done"""
        messageFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="groove")
        messageFrame.grid(row=2, column=2,  padx=5, pady=5)
        self.messageVar = StringVar()
        self.messageVar.set("")
        message = Label(messageFrame, textvariable=self.messageVar, width=50, height=5, wraplength = 300)
        message.grid(row=1, column=1)


    def _initGridBuildingTools(self):
        """Sets up the tools for modifying the grid and the number of agents"""
        gridSetupFrame = Frame(self.root, bd=5, padx=5, pady=5, relief="groove")
        gridSetupFrame.grid(row=2, column=1, padx=5, pady=5, sticky=N)
        editTitle = Label(gridSetupFrame, text="Sim Builder Options", font="Arial 16 bold", anchor = CENTER)
        editTitle.grid(row=0, column=1, padx=5, pady=5)

        # Make a new subframe
        makerFrame = Frame(gridSetupFrame, bd=2, relief="groove", padx=5, pady=5)
        makerFrame.grid(row=1, column=1, padx=5, pady=5)

        sizeLabel = Label(makerFrame, text="Grid Dim")
        self.gridDimensionText = IntVar()
        self.gridDimensionText.set(str(self.gridDim))
        self.rowsEntry = Entry(makerFrame, textvariable=self.gridDimensionText, width=4, justify=CENTER)
        agentsLabel = Label(makerFrame, text="Agents")
        self.agentNum = IntVar()
        self.agentNum.set(self.numberAgents)
        self.numAgents = Entry(makerFrame, textvariable=self.agentNum, width=4, justify=CENTER)

        self.gridButton = Button(makerFrame, text="New Grid", command=self.resetGridWorld)

        # place the basic widgets for setting up the grid and agents
        sizeLabel.grid(row=1, column=3)
        agentsLabel.grid(row=2, column=3)
        self.rowsEntry.grid(row=1, column=4)
        self.numAgents.grid(row=2, column=4)
        self.gridButton.grid(row=3, column=3, columnspan=2, pady=5)



    def _initGrid(self):
        """sets up the grid with current assigned dimensions, and number of agents
        done as a helper because it may need to be done over later"""
        self.canvas = None
        self.canvasSize = 500
        self.canvasPadding = 10
        canvasFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="raise", bg="lemon chiffon")
        canvasFrame.grid(row=3, column=2, rowspan=3, padx=5, pady=5)
        self.canvas = Canvas(canvasFrame,
                             width=self.canvasSize + self.canvasPadding,
                             height=self.canvasSize + self.canvasPadding)
        self.canvas.grid(row=1, column=1)

        self._buildTkinterGrid()


    def _initSimTools(self):
        """Sets up the search frame, with buttons for selecting which search, for starting a search,
        stepping or running it, and quitting from it.  You can also choose how many steps should happen
        for each click of the "step" button"""
        simFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="groove")
        simFrame.grid(row=3, column=1, padx=5, pady=5)
        simTitle = Label(simFrame, text="Sim Options", font="Arial 16 bold")
        simTitle.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # Sets the maximum
        stepsLabel = Label(simFrame, text="Max sim steps")
        self.maxStepsText = IntVar()
        self.maxStepsText.set(self.maxSteps)
        self.stepsEntry = Entry(simFrame, textvariable=self.maxStepsText, width=4, justify=CENTER)
        stepsLabel.grid(row=1, column=1)
        self.stepsEntry.grid(row=1, column=2)

        delayLabel = Label(simFrame, text="Step delay")
        self.delayText = StringVar()
        self.delayText.set("{0:4.2f}".format(self.delayTime))
        self.delayEntry = Entry(simFrame, textvariable=self.delayText, width=5, justify=CENTER)
        delayLabel.grid(row=2, column=1)
        self.delayEntry.grid(row=2, column=2)

        gapLabel = Label(simFrame, text="", width=20, bg="light gray")
        gapLabel.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.currStepsText = IntVar()
        self.currStepsText.set(self.currSteps)
        currStepLabel = Label(simFrame, text="Current steps:")
        currSteps = Label(simFrame, textvariable=self.currStepsText, width=4, justify=CENTER, relief="raised")
        currStepLabel.grid(row=5, column=1)
        currSteps.grid(row=5, column=2)

        self.stepButton = Button(simFrame, text="Step simulation", command=self.stepSimulation)
        self.stepButton.grid(row=6, column=1, columnspan=2, pady=5)

        self.runButton = Button(simFrame, text="Run simulation", command=self.runSimulation)
        self.runButton.grid(row=7, column=1, columnspan=2, pady=5)



    def _initSearchTools(self):
        """Sets up the search frame, with buttons for selecting which search, for starting a search,
        stepping or running it, and quitting from it.  You can also choose how many steps should happen
        for each click of the "step" button"""
        searchFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="groove")
        searchFrame.grid(row=4, column=1, padx=5, pady=5, sticky=N)
        searchTitle = Label(searchFrame, text="Search Options", font="Arial 16 bold")
        searchTitle.grid(row=0, column=1, padx=5, pady=5)
        self.searchType = StringVar()
        self.searchType.set("hillClimb")

        hillClimbButton = Radiobutton(searchFrame, text="Hill-Climbing",
                                      variable=self.searchType, value="hillClimb")
        beamButton = Radiobutton(searchFrame, text="Beam Search",
                                 variable=self.searchType, value="beam")
        gaButton = Radiobutton(searchFrame, text="Genetic Alg",
                               variable=self.searchType, value="ga")
        hillClimbButton.grid(row=1, column=1, sticky=W)
        beamButton.grid(row=2, column=1, sticky=W)
        gaButton.grid(row=3, column=1, sticky=W)

        resetSearch = Button(searchFrame, text="Set Up Search", command=self.resetSearch)

        self.stepSearch = Button(searchFrame, text="Step Search", command=self.stepSearch, state=DISABLED)
        self.runSearch = Button(searchFrame, text="Run Search", command=self.runSearch, state=DISABLED)
        self.quitSearch = Button(searchFrame, text="Quit Search", command=self.quitSearch, state=DISABLED)
        resetSearch.grid(row=13, column=1, pady=5)
        self.stepSearch.grid(row=15, column=1)
        self.runSearch.grid(row=16, column=1)
        self.quitSearch.grid(row=17, column=1)
        self.currentSearch = None
        self.currentSearcher = None
        self.currentNode = None

    ### =================================================================
    ### The following are callbacks for buttons

    def quit(self):
        """Callback for the quit button: destroy everything"""
        self.root.destroy()

    # ----------------------------------------------------------------
    # Button callbacks for Edit buttons

    def resetGridWorld(self, ruleString=None):
        """This is both a callback for the New Grid button, but also called from other
        places where the ruleString is set to a non-None value"""
        self._removeGridItems()

        size = self.gridDimensionText.get()
        ageNum = self.agentNum.get()
        try:
            self.gridDim = int(size)
            self.numberAgents = int(ageNum)
        except:
            self._postMessage("Dimension must be positive integer.")
            return
        self.sim = ALifeSim(self.gridDim, self.numberAgents, rulesets=[ruleString] * self.numberAgents)
        self._buildTkinterGrid()
        self.currSteps = 0
        self.currStepsText.set(self.currSteps)
        self.currentSearch = None

    # ----------------------------------------------------------------
    # Button callbacks for Search buttons

    def resetSearch(self):
        """This is a callback for the Set Up Search button. It resets the simulation based on the current
        values, and sets up the algorithm to be called, it initializes the search.
        It disables the grid editing and turns off the edit mode, and turns on the search mode"""

        self._clearMessage()

        self.resetGridWorld()
        self.currentNode = None
        self.currentSearch = self.searchType.get()
        print(self.currentSearch)
        if self.currentSearch == "hillClimb":
            self.currentSearcher = HillClimber(RulesetState(self.evalRulestring, self.maxSteps))
        elif self.currentSearch == 'beam':
            pass
        elif self.currentSearch == 'ga':    # TODO: You will need to update this analogous to the HillClimber
            pass

        self._disableChanges()
        self._enableSearch()


    def evalRulestring(self, ruleString):
        """Evaluates a given rule string by using it to create agents and running a simulation with those agents."""
        self.resetGridWorld(ruleString)
        self._postMessage("Testing rulestring: " + str(ruleString))
        self.runSimulation()
        return self.avgTime


    def runSearch(self):
        """This callback for the Run Search button keeps running steps of the search until the search is done
        or a problem crops up.  """
        keepLooping = True
        while keepLooping:
            keepLooping = self._handleOneStep()


    def stepSearch(self):
        """This repeats the current stepCount number of steps of the search, stopping after that.
        Otherwise, this is very similar to the previous function"""
        keepLooping = self._handleOneStep()


    def _handleOneStep(self):
        """This helper helps both the run search and step search callbacks, by handling the
        different outcomes for one step of the search.  """
        status = self.currentSearcher.step()
        count = self.currentSearcher.getCount()
        nextState = self.currentSearcher.getCurrState()
        nextValue = self.currentSearcher.getCurrValue()
        keepGoing = True
        if status == "local maxima":
            self._addMessage("Local maxima found after " + str(count) + " steps: " + str(nextState))
            keepGoing = False
            self.root.update()
            time.sleep(0.5)
        elif status == "optimal":
            self._addMessage("Optimal solution found after " + str(count) + " steps: " + str(nextState))
            # self.wrapUpSearch(nextState, nextValue)
            keepGoing = False
            self.root.update()
            time.sleep(0.5)
        else:
            self._addMessage("Search continuing after " + str(count) + " steps.")
            self.root.update()
            time.sleep(0.5)

        return keepGoing

    def wrapUpSearch(self, nextState, nextValue):
        """This produces the ending statistics, finds and marks the final path, and then closes
        down the search so it will not continue"""
        pass
        #
        # printStr = "Total path cost = %d      " % totalCost
        # printStr += "Path length = %d\n" % len(finalPath)
        # printStr += "Nodes created = %d      " % self.currentSearcher.getNodesCreated()
        # printStr += "Nodes visited = %d" % self.currentSearcher.getNodesVisited()
        # self._postMessage(printStr)
        # self.currentSearch = None
        # self.currentNode = None
        #


    def quitSearch(self):
        """A callback for clearing away the search and returning to edit mode"""
        self._disableSearch()
        self._enableChanges()
        self.currentSearch = None
        self.currentNode = None
        self._clearMessage()

    ### =================================================================
    ### Helper functions for running simulation


    def runSimulation(self):
        """Runs the simulation until either all agents die or we reach the max number of steps."""
        self.maxSteps=int(self.maxStepsText.get())
        self.delayTime = float(self.delayText.get())
        while self.currSteps <= self.maxSteps:
            result = self.stepSimulation()
            self.root.update()
            time.sleep(self.delayTime)
            if not result:
                break
        self.reportSimResult()
        self.root.update()
        time.sleep(0.5)




    def stepSimulation(self):
        """Runs one step of the simulation, then updates the grid with new colors and moving agents."""
        self.sim.step()
        for row in range(self.gridDim):
            for col in range(self.gridDim):
                food = self.sim.foodAt(row, col)
                cellColor = self._determinePatchColor(food, self.sim.MAX_FOOD)
                patchId = self.posToPatchId[row, col]
                self.canvas.itemconfig(patchId, fill=cellColor)
        if len(self.sim.getAgents()) == 0:
            return False
        for agent in self.sim.getAgents():
            agColor = self._determineAgentColor(agent.getEnergy())
            id = agent.getVisId()
            self.canvas.itemconfig(id, fill=agColor)
            (oldRow, oldCol, oldHead) = self.agentIdToPose[id]
            (newRow, newCol, newHead) = agent.getPose()
            (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)
            offsetCoords = self._determineAgentCoords(agent)
            coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]
            flatCoords = [n for subl in coords for n in subl]
            self.canvas.coords(id, flatCoords)
            self.canvas.lift(id)

            self.agentIdToPose[id] = agent.getPose()
        self.currSteps += 1
        self.currStepsText.set(self.currSteps)
        return True


    def reportSimResult(self):
        """Reports statistics on how the simulation came out."""
        total = 0
        count = 0
        self.minTime = 10 * self.maxSteps
        self.maxTime = 0
        deadAgents = self.sim.getDeadAgents()
        self.agentsLiving = self.sim.getAgents()
        numLiving = len(self.agentsLiving)
        for agent, when in deadAgents:
            if when < self.minTime:
                self.minTime = when
            if when > self.maxTime:
                self.maxTime = when
            total += when
            count += 1
        self.avgTime = (total + numLiving*self.maxSteps) / self.numberAgents
        if numLiving > 0:
            maxTime = self.maxSteps
        message1Template = "Survival time in steps: Average = {0:5.2f}     Minimum = {1:3d}     Maximum = {2:3d}"
        message1 = message1Template.format(round(self.avgTime, 2), self.minTime, self.maxTime)
        message2Template = "Number living = {0:5d}"
        message2 = message2Template.format(numLiving)
        self._addMessage(message1 + '\n' + message2)


    ### =================================================================
    ### Private helper functions


    def _buildTkinterGrid(self):
        """This sets up the display of the grid, based on the simulation object.
        Re-called when dimensions changed."""
        self.patchIdToPos = {}
        self.posToPatchId = {}
        self.agentIdToPose = {}

        if self.gridDim * 50 < self.canvasSize:
            self.cellSize = 50
        else:
            self.cellSize = self.canvasSize / self.gridDim

        for row in range(self.gridDim):
            for col in range(self.gridDim):
                (x1, y1, x2, y2) = self._posToCoords(row, col)
                food = self.sim.foodAt(row, col)
                cellColor = self._determinePatchColor(food, self.sim.MAX_FOOD)
                currId = self.canvas.create_rectangle(x1, y1, x2, y2, fill=cellColor)
                self.patchIdToPos[currId] = (row, col)
                self.posToPatchId[row, col] = currId
                agents = self.sim.agentsAt(row, col)
                for ag in agents:
                    offsetCoords = self._determineAgentCoords(ag)
                    agColor = self._determineAgentColor(ag.getEnergy())
                    coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]
                    agId = self.canvas.create_polygon(coords,fill=agColor)
                    self.agentIdToPose[agId] = ag.getPose()
                    # print('orig coords:', coords)
                    # print("agent pose:", ag.getPose())
                    ag.setVisId(agId)


    def _determineAgentCoords(self, agent):
        """gives offset coordinates based on the direction the agent is
        pointing."""
        (agr, agc, heading) = agent.getPose()
        oneSixth = self.cellSize / 6
        fiveSixths = 5 * oneSixth
        half = self.cellSize / 2
        quarter = self.cellSize / 4
        threeQ = 3 * quarter

        if heading == 'n':
            return [(half, oneSixth), (quarter, fiveSixths), (threeQ, fiveSixths)]
        elif heading == 'e':
            return [(fiveSixths, half), (oneSixth, quarter), (oneSixth, threeQ)]
        elif heading == 's':
            return [(half, fiveSixths), (threeQ, oneSixth), (quarter, oneSixth)]
        elif heading == 'w':
            return [(oneSixth, half), (fiveSixths, threeQ), (fiveSixths, quarter)]
        else:
            print("Bad heading for agent", heading)


    def _determinePatchColor(self, foodAt, maxFood):
        if foodAt == 0:
            cellColor = "white"
        else:
            diff = maxFood - foodAt
            if diff < 0:
                diff = 0
            ratio = diff / maxFood
            greenColor = int((ratio * 245) + 10)
            cellColor = "#%02x%02x%02x" % (0, greenColor, 0)

        return cellColor

    def _determineAgentColor(self, energy):
        if energy <= 0:
            color = 'black'
        else:
            if energy > 60:
                energy = 60
            ratio = energy / 60
            redColor = int((ratio * 245) + 10)
            color = "#%02x%02x%02x" % (redColor, 0, 0)
        return color



    def _disableChanges(self):
        """Turn off access to the edit operations, by setting each of the GUI elements to DISABLED"""
        self.changesEnabled = False
        self.rowsEntry.config(state=DISABLED)
        self.numAgents.config(state=DISABLED)
        self.gridButton.config(state=DISABLED)

        self.stepsEntry.config(state=DISABLED)
        self.delayEntry.config(state=DISABLED)
        self.stepButton.config(state=DISABLED)
        self.runButton.config(state=DISABLED)


    def _enableChanges(self):
        """Turn on access to the edit operations, by setting each GUI element to NORMAL"""
        self.changesEnabled = True
        self.rowsEntry.config(state=NORMAL)
        self.numAgents.config(state=NORMAL)
        self.gridButton.config(state=NORMAL)

        self.stepsEntry.config(state=NORMAL)
        self.delayEntry.config(state=NORMAL)
        self.stepButton.config(state=NORMAL)
        self.runButton.config(state=NORMAL)

    def _disableSearch(self):
        """Turn off the search operations, by setting each GUI element to DISABLED."""
        self.stepSearch.config(state=DISABLED)
        self.runSearch.config(state=DISABLED)
        self.quitSearch.config(state=DISABLED)

    def _enableSearch(self):
        """Turn on the search operations, by setting each GUI element to NORMAL"""
        self.stepSearch.config(state=NORMAL)
        self.runSearch.config(state=NORMAL)
        self.quitSearch.config(state=NORMAL)

    def _removeGridItems(self):
        """A helper that removes all the grid cell objects from the maze, prior to creating new
        ones when the simulation is reset."""
        for row in range(self.gridDim):
            for col in range(self.gridDim):
                currId = self.posToPatchId[row, col]
                self.canvas.delete(currId)
        for id in self.agentIdToPose:
            self.canvas.delete(id)
        self.canvas.update()
        self.posToPatchId = {}
        self.patchIdToPos = {}
        self.agentIdToPose = {}




    # -------------------------------------------------
    # Utility functions


    def _postMessage(self, messageText):
        """Posts a message in the message box"""
        self.messageVar.set(messageText)

    def _clearMessage(self):
        """Clears the message in the message box"""
        self.messageVar.set("")
        
    def _addMessage(self, messageText):
        oldMessage = self.messageVar.get()
        newMessage = oldMessage + '\n' + messageText
        self.messageVar.set(newMessage)


    def _setCellColor(self, cellId, color):
        """Sets the grid cell with cellId, and at row and column position, to have the
        right color.  Note that in addition to the visible color, there is also a colors 
        matrix that mirrors the displayed colors"""
        self.canvas.itemconfig(cellId, fill = color)


    def _setOutlineColor(self, cellId, color):
        """Sets the outline of the grid cell with cellID, and at row and column position, to
        have the right color."""
        self.canvas.itemconfig(cellId, outline=color)



    def _posToId(self, row, col):
        """Given row and column indices, it looks up and returns the GUI id of the cell at that location"""
        return self.posToPatchId[row, col]

    def _idToPos(self, currId):
        """Given the id of a cell, it looks up and returns the row and column position of that cell"""
        return self.patchIdToPos[currId]

    
    def _posToCoords(self, row, col):
        """Given a row and column position, this converts that into a position on the frame"""
        x1 = col * self.cellSize + 5
        y1 = row * self.cellSize + 5
        x2 = x1 + (self.cellSize - 2)
        y2 = y1 + (self.cellSize - 2)
        return (x1, y1, x2, y2)

    def _coordToPos(self, x, y):
        """Given a position in the frame, this converts it to the corresponding row and column"""
        col = (x - 5) / self.cellSize
        row = (y - 5) / self.cellSize
        if row < 0:
            row = 0
        elif row >= self.gridDim:
            row = self.gridDim - 1

        if col < 0:
            col = 0
        elif col >= self.gridDim:
            col = self.gridDim - 1
            
        return (int(row), int(col))





# The lines below cause the maze to run when this file is double-clicked or sent to a launcher, or loaded
# into the interactive shell.
if __name__ == "__main__":
    s = ALifeGUI(20, 20)
    s.setupWidgets()
    s.goProgram()
