function [I] = ImageCompression(filename, modes)
%ImageComression does a Singular Value Decomposiotion and rebuilds the
%picture with less Singular Values
%input arguments:
%filename = filename of the image that should be compressed
%modes = number of modes that should stay
%output arguments:
%I = compressed image
    
    %import image
    image = imread(filename);
    imageDouble = im2double(image);
    
    %split picture in red, green and blue picture
    red = imageDouble(:,:,1);
    green = imageDouble(:,:,2);
    blue = imageDouble(:,:,3);
    
    %sdv of all matrix and recombining with less modes
    [M.UR,M.SR,M.VR] = svd(red);
    iRed = M.UR(:,1:modes)*M.SR(1:modes,1:modes)*M.VR(:,1:modes)';
    [M.UG,M.SG,M.VG] = svd(green);
    iGreen = M.UG(:,1:modes)*M.SG(1:modes,1:modes)*M.VG(:,1:modes)';
    [M.UB,M.SB,M.VB] = svd(blue);
    iBlue = M.UB(:,1:modes)*M.SB(1:modes,1:modes)*M.VB(:,1:modes)';
    
    %recombining of red, green and blue picture to one
    I = cat(3,iRed,iGreen,iBlue);
    
    %show orginal and compressed picture
    picture = figure(1);
    hold on;
    subplot(1,3,1);
    imshow(image);
    title('Orginal')
    subplot(1,3,2);
    imshow(I);
    tit = sprintf('Reduced with %i SV', max(modes));
    title(tit)
    
    % singular Values of picture
    [m,n] = size(M.SR);
    s3 = subplot(1,3,3);
    set(s3, 'position', [0.68 0.35 0.25 0.35]);
    SV.line1 = semilogy(diag(M.SR), 'k');
    hold on;
    SV.line2 = semilogy(diag(M.SR(1:modes,1:modes)), 'r');
    title('Singular Values');
    
    % add slider to change SV randomly
    random = 0;
    SV.rSlider = uicontrol('style','slider','min',-50,'max',50,'Value',...
        random,'Units','normalized','position',[0.1 0.08 0.7 0.05]);
    
    % add slider to change used SV
    SV.mSlider = uicontrol('style','slider','min', 1, 'max', min(m,n),...
        'Value', modes,'Units','normalized','position',[0.1 0.2 0.7 0.05],...
        'Callback', {@changeplot,SV,M,picture});
    bgcolor = picture.Color;
    SV.bl1 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.05,0.19,0.05,0.05],'String','1','BackgroundColor',bgcolor);
    SV.bl2 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.81,0.19,0.05,0.05],'String',min(m,n),'BackgroundColor',bgcolor);
    SV.bl3 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.35,0.14,0.2,0.05],'String','Used modes','BackgroundColor',bgcolor);
    
    % add slider to change SV randomly
    set(SV.rSlider, 'Callback', {@changerandom,SV,M,picture});
    SV.bl1 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.04,0.07,0.05,0.05],'String','-50%','BackgroundColor',bgcolor);
    SV.bl2 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.81,0.07,0.05,0.05],'String','50%','BackgroundColor',bgcolor);
    SV.bl3 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.35,0.02,0.2,0.05],'String','Random changes','BackgroundColor',bgcolor);
    
    % add button to set the sliders on there origin settings
    SV.button = uicontrol('Units','normalized','position',[0.9 0.17 0.05 0.05],...
        'Callback',{@originSettings,modes,SV,M,picture});
    SV.bl3 = uicontrol('Parent',picture,'Style','text','Units','normalized',...
        'Position',[0.88,0.06,0.1,0.1],'String','Orgin Settings','BackgroundColor',bgcolor);
end

function changeplot(source, event, SV, M, picture)
%changeplot is a help function for ImageCompession. It changes the
%plots when the slider for the used modes was used
%input arguments:
%source, event = outputs of the slider
%SV = plot of singular values
%M = set of all U,S,V from the svds
%picture = plot of the pictures

    %redraw plots for new modes
    modes = 1:int16(source.Value);
    redrawplot(modes, SV, M, picture, true);
    set(SV.rSlider, 'Value', 0)
end

function changerandom(source, event, SV, M, picture)
%changerandom is a help function for ImageCompession. It changes the
%plots when the slider for the random SV was used
%input arguments:
%source, event = outputs of the slider
%SV = plot of singular values
%M = set of all U,S,V from the svds
%picture = plot of the pictures
    len = SV.mSlider.Value;
    numbersToChange = source.Value * len / 100;
    modes = 1:int16(len);
    if(numbersToChange < 0)
        for i = 1:int16(norm(numbersToChange))
            del = int16(rand * (len-1)) + 1;
            modes = setdiff(modes, modes(1, del));
            len = len - 1;
        end
    elseif(numbersToChange > 0)
        finalSize = len+int16(numbersToChange);
        while(length(modes) ~= finalSize)
            len = length(modes);
            unused = min(size(M.SR)) - len;
            numbersToChange = finalSize - len;
            addNumbers = rand([1 numbersToChange]) * unused + len;
            modes = [modes, addNumbers];
            modes = unique(modes);
        end
    end
    redrawplot(modes, SV, M, picture, false);
end

function originSettings(button, EventData, modes, SV, M, picture)
%orginSettings is a help function for ImageCompession. It sets the sliders
%back to there origin settings
%input arguments:
%button, EventData = outputs of the slider
%modes = orgin setting of the modes
%SV = plot of singular values
%M = set of all U,S,V from the svds
%picture = plot of the pictures
    set(SV.mSlider, 'Value', modes);
    set(SV.rSlider, 'Value', 0);
    redrawplot(1:modes, SV, M, picture, true)
end

function redrawplot(modes, SV, M, picture, drawSV)
    %redraw singular value plot
    if(drawSV)
        s3 = subplot(1,3,3);
        set(s3, 'position', [0.68 0.35 0.25 0.35]);
        SV.line1 = semilogy(diag(M.SR), 'k');
        hold on;
        SV.line2 = semilogy(diag(M.SR(modes,modes)), 'r');
        title('Singular Values');
    end
    
    %recalculate the compressed picture
    iRed = M.UR(:,modes)*M.SR(modes,modes)*M.VR(:,modes)';
    iGreen = M.UG(:,modes)*M.SG(modes,modes)*M.VG(:,modes)';
    iBlue = M.UB(:,modes)*M.SB(modes,modes)*M.VB(:,modes)';
    I = cat(3,iRed,iGreen,iBlue);
    
    %redraw the compressed picture
    subplot(1,3,2);
    imshow(I);
    tit = sprintf('Reduced with %i SV', max(modes));
    title(tit)
end

