function cost = cost1D(a0, Kn, tno, Gnc, rangeCOD)
    % cost = 100*abs(area predicted-area experiment)/area experiment 
    %        calculated in DCBCZMparams.py using Abaqus
    % Write the "full" state for DCBCZMparams.py to read it
    fs = fopen('state.txt','w');
    fprintf(fs, '%g %g %g %g %g\n', a0, Kn, tno, Gnc, rangeCOD );
    fclose(fs);% If Python error, use %.4f to avoid writing an integer
    % Execute "DCBCZMparams.py"
    [~, ~] = dos('abaqus cae -nogui DCBCZMparams.py');
    % Don't open until Abaqus is finished +> Job.waitForCompletion()
    fr = fopen('cost.txt','r');
    cost = fscanf(fr, '%g');% read the error calculated by DCBCZMparams.py
    disp([num2str([a0, Kn, tno, Gnc, cost])])
    fclose(fr);
end
